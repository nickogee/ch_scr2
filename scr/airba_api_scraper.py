from typing import Any, Dict, List, Optional, Set, Tuple
import datetime
from scr.airba_fetch import PAGE, CATALOG, WORKFLOW, URL_CATEGORY, PARAMS_CATEGORY, REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm_air, update_category_mgm_air, update_parent_category_mgm_air
from constants.constants import DB_PATH, DB_AIR_CATEGORY_TABLE, DB_AIR_CATEGORY_CREATE_STR, MERCANTS, DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX


def clean_string(text: Optional[str]) -> str:
    """Remove unwanted characters from a string."""
    if not text:
        return ''
    for ch in ['«', '»', '"', "'"]:
        text = text.replace(ch, '')
    return text


def make_category_dict(parent_id: str, id_: str, name: str, level: str) -> Dict[str, str]:
    """Create a category dictionary."""
    return {
        'parent_id': parent_id,
        'id': id_,
        'name': name,
        'category_lvl': level,
    }


class AirbaScrapper:
    """
    Scraper for Airba categories and products.
    """
    def __init__(self, fast_category_id: Optional[str] = None) -> None:
        self.date_time_now: datetime.datetime = datetime.datetime.now()
        self.rezult: List[Dict[str, Any]] = []
        self.category_list: List[Dict[str, str]] = []
        self.category_update: List[Dict[str, Any]] = []
        self.fast_category_id: Optional[str] = fast_category_id
        self.limit_off: bool = bool(fast_category_id)
        self.workflow: str = WORKFLOW
        self.city: str = 'almaty'

    def fill_category_table(self) -> None:
        """
        Create and populate the category table with current data if it does not exist.
        """
        if table_exists(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE):
            return
        params_head = PARAMS_CATEGORY.copy()
        params_head['headers']['workflow'] = self.workflow
        resp = get_fetch(url=URL_CATEGORY, params=params_head)
        resp_js = resp.json()
        data = resp_js['data']
        for head_dct in data:
            if head_dct['id'] == 0:
                continue
            head_id = str(head_dct['id'])
            self.category_list.append(make_category_dict('', head_id, str(head_dct['section']), '1'))
            print(f"- Получаем категорию id={head_dct['id']}, name={head_dct['section']}")
            chld_ls = head_dct.get('categories')
            if chld_ls:
                for chld_dct in chld_ls:
                    chld_id = str(chld_dct['id'])
                    self.category_list.append(make_category_dict(head_id, chld_id, str(chld_dct['name']), '2'))
                    print(f"-- Получаем категорию id={chld_dct['id']}, name={chld_dct['name']}")
                    self._process_subcategories(chld_id, chld_dct['items'])
        if self.category_list:
            upload_to_db(
                rezult=self.category_list,
                db_path=DB_PATH,
                table_name=DB_AIR_CATEGORY_TABLE,
                table_create_str=DB_AIR_CATEGORY_CREATE_STR,
                pk_column='id'
            )

    def _process_subcategories(self, chld_id: str, sub_chld_ls: List[Dict[str, Any]]) -> None:
        for sub_chld_dct in sub_chld_ls:
            sub_chld_id = str(sub_chld_dct['id'])
            self.category_list.append(make_category_dict(chld_id, sub_chld_id, str(sub_chld_dct['name']), '3'))
            print(f"--- Получаем категорию id={sub_chld_dct['id']}, name={sub_chld_dct['name']}")
            rand_pause(10)
            params_chld = PARAMS_CATEGORY.copy()
            params_chld['headers']['workflow'] = self.workflow
            chld_resp = get_fetch(url=f'{URL_CATEGORY}{sub_chld_id}/', params=params_chld)
            chld_resp_js = chld_resp.json()
            chld_data = chld_resp_js['data']
            for i in chld_data:
                i_id = str(i['id'])
                self.category_list.append(make_category_dict(sub_chld_id, i_id, str(i['name']), '4'))
                print(f"---- Получаем категорию id={i['id']}, name={i['name']}")

    def fill_category_data(self) -> None:
        """
        Parse product data for the required categories.
        """
        self.category_list = get_next_categoy_list_mgm_air(
            db_path=DB_PATH,
            table_name=DB_AIR_CATEGORY_TABLE,
            mercant='air',
            cat_lvl='3',
            fast_category_id=self.fast_category_id
        )
        req_cnt = 0
        for cat_tpl in self.category_list:
            if (not self.limit_off) and (req_cnt > REQ_LIMIT):
                break
            catalog_di = cat_tpl[0]
            is_last_page = False
            page = 1
            while not is_last_page:
                params = self._prepare_catalog_params(catalog_di, page)
                resp = get_fetch(url=URL_CATALOG, params=params)
                req_cnt += 1
                page += 1
                if resp.status_code == 200:
                    is_last_page = self._process_product_page(resp, cat_tpl, catalog_di, page, req_cnt)
                else:
                    is_last_page = True
                print(f'Fresh Airba - страница {page - 1} категории "{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}" запрос {req_cnt}')
                rand_pause()
            self._update_category_scrap_count(cat_tpl)

    def _prepare_catalog_params(self, catalog_di: Any, page: int) -> Dict[str, Any]:
        params = PARAMS_CATALOG.copy()
        param_path = params['headers']['path']
        param_path = param_path.replace(PAGE, str(page))
        param_path = param_path.replace(CATALOG, str(catalog_di))
        params['headers']['path'] = param_path
        params['headers']['workflow'] = self.workflow
        params['params']['category'] = str(catalog_di)
        params['params']['page'] = str(page)
        return params

    def _process_product_page(self, resp: Any, cat_tpl: Tuple, catalog_di: Any, page: int, req_cnt: int) -> bool:
        resp_js = resp.json()
        data = resp_js.get('data')
        if not data:
            return True
        products = data.get('products')
        if not products:
            return True
        products_page = products.get('page')
        products_total_page = products.get('total_pages')
        is_last_page = (products_page == products_total_page)
        results_ls = products.get('results')
        if results_ls:
            for prod_dct in results_ls:
                self.rezult.append(self._parse_product(prod_dct, cat_tpl))
        return is_last_page

    def _parse_product(self, prod_dct: Dict[str, Any], cat_tpl: Tuple) -> Dict[str, Any]:
        title = clean_string(prod_dct.get('name'))
        description = clean_string(prod_dct.get('description'))
        images_ls = prod_dct.get('images')
        image = images_ls[0]['image_origin_url'] if images_ls else ''
        category_dct = prod_dct.get('category')
        category_full_path = category_dct.get('full_hierarchy') if category_dct else f'{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}'
        prev_cost = prod_dct.get('price_previous')
        prev_cost = int(prev_cost) if isinstance(prev_cost, (int, float)) else 0
        brand = clean_string(str(prod_dct.get('brand')))
        mercant_short_name = 'air' + '-' + CITY_POSTFIX[self.city]
        return {
            'mercant_id': MERCANTS[mercant_short_name],
            'mercant_name': mercant_short_name,
            'product_id': str(self.city + '_' + str(prod_dct.get('id'))),
            'id': str(prod_dct.get('id')),
            'title': title,
            'description': description,
            'url': '',
            'url_picture': str(image),
            'time_scrap': str(datetime.datetime.now().isoformat()),
            'sub_category': cat_tpl[1],
            'category_full_path': category_full_path,
            'brand': brand,
            'cost': str(int(prod_dct.get('price_actual'))),
            'prev_cost': str(prev_cost),
            'measure': prod_dct.get('unit_measurement'),
            'city': self.city,
        }

    def _update_category_scrap_count(self, cat_tpl: Tuple) -> None:
        d = {
            'id': cat_tpl[0],
            'scrap_count': cat_tpl[4] + 1
        }
        self.category_update.append(d)

    def __upload_to_db(self) -> None:
        """
        Upload parsed data to the database and update scrap counts for categories.
        """
        print(f'Fresh Airba - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')
        update_category_mgm_air(self.category_update, DB_PATH, DB_AIR_CATEGORY_TABLE, 'id')
        self._update_parent_categories(6)
        self._update_parent_categories(7)
        self._update_parent_categories(7)  # This is repeated in the original code

    def _update_parent_categories(self, idx: int) -> None:
        parent_set: Set[Any] = {i[idx] for i in self.category_list}
        for par_id in parent_set:
            filter_tpl = ('parent_id', par_id)
            update_parent_category_mgm_air(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl)

    def start(self) -> None:
        """
        Run the full scraping process: fill categories, fetch data, upload to DB.
        """
        self.fill_category_table()
        self.fill_category_data()
        self.__upload_to_db()


def fast_category_scraper() -> None:
    """
    Run the scraper for a predefined list of fast categories.
    """
    fast_category_ls = [
        '1782',  # Фрукты, ягоды
        '1785'   # Овощи, грибы и зелень
    ]
    for fast_category in fast_category_ls:
        airba = AirbaScrapper(fast_category)
        airba.start()


def main() -> None:
    """
    Main entry point for the Airba scraper.
    """
    airba = AirbaScrapper()
    airba.start()


if __name__ == '__main__':
    main() 