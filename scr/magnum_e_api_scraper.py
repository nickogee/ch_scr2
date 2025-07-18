import datetime
from scr.magnum_e_fetchs import PARAMS_TOKEN, URL_TOKEN, URL_CATEGORY, PARAMS_CATEGORY, \
    REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm_air, \
    update_category_mgm_air, update_parent_category_mgm_air
from constants.constants import DB_PATH, DB_MGM_E_CATEGORY_TABLE, DB_MGM_E_CATEGORY_CREATE_STR, MERCANTS, \
    DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX

class MagnumExpressScraper:
    """
    Scraper for Magnum Express API. Handles category and product data extraction and database upload.
    """
    def __init__(self, fast_category_id=None):
        self.city = 'almaty'
        self.fast_category_id = fast_category_id
        self.limit_off = bool(fast_category_id)
        self.category_list = []
        self.category_update = []
        self.results = []
        self.token = None
        self.date_time_now = datetime.datetime.now()
        self.get_token()

    def get_token(self):
        """
        Obtain and set the API token for requests.
        """
        if not self.token:
            resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
            resp_js = resp.json()
            self.token = resp_js.get('token')

    def ensure_category_table(self):
        """
        Ensure the category table exists and is populated with current data.
        """
        if table_exists(db_path=DB_PATH, table_name=DB_MGM_E_CATEGORY_TABLE):
            return
        params_head = PARAMS_CATEGORY.copy()
        params_head['params']['parentId'] = ''
        params_head['headers']['Authorization'] = self.token
        resp = get_fetch(url=URL_CATEGORY, params=params_head)
        resp_js = resp.json()
        for head_cat in resp_js:
            self.category_list.append(self._make_category_dict(head_cat, '1', ''))
            print(f"Получаем категорию id={head_cat['id']}, name={head_cat['name']}")
            for chld_cat in head_cat.get('childCategories', []):
                self.category_list.append(self._make_category_dict(chld_cat, '2', chld_cat['parentId']))
                print(f"Получаем категорию id={chld_cat['id']}, name={chld_cat['name']}")
        if self.category_list:
            upload_to_db(
                rezult=self.category_list,
                db_path=DB_PATH,
                table_name=DB_MGM_E_CATEGORY_TABLE,
                table_create_str=DB_MGM_E_CATEGORY_CREATE_STR,
                pk_column='id'
            )

    def _make_category_dict(self, cat, lvl, parent_id):
        return {
            'parent_id': str(parent_id) if parent_id else str(cat.get('parentId', '')),
            'id': str(cat['id']),
            'name': str(cat['name']),
            'category_lvl': lvl,
        }

    def fetch_category_data(self):
        """
        Fetch product data for each category and store results in self.results.
        """
        self.category_list = get_next_categoy_list_mgm_air(
            db_path=DB_PATH,
            table_name=DB_MGM_E_CATEGORY_TABLE,
            mercant='mgm_e',
            cat_lvl='2',
            fast_category_id=self.fast_category_id
        )
        req_cnt = 0
        for cat_tpl in self.category_list:
            if not self.limit_off and req_cnt > REQ_LIMIT:
                break
            for page in range(21):
                params = PARAMS_CATALOG.copy()
                params['params']['categoryIds'] = cat_tpl[0]
                params['params']['pageId'] = str(page)
                params['headers']['Authorization'] = self.token
                resp = get_fetch(url=URL_CATALOG, params=params)
                resp_js = resp.json()
                req_cnt += 1
                content = resp_js.get('content')
                if content:
                    for prod in content:
                        self.results.append(self._parse_product(prod, cat_tpl))
                else:
                    self.category_update.append({
                        'id': cat_tpl[0],
                        'scrap_count': cat_tpl[4] + 1
                    })
                    break
                print(f'Magnum express {self.city} - страница {page + 1} категории "{cat_tpl[2]}/{cat_tpl[1]}" запрос {req_cnt}')
                rand_pause()

    def _parse_product(self, prod, cat_tpl):
        def clean(text):
            if not text:
                return ''
            return text.replace('«', '').replace('»', '').replace('"', '').replace("'", '')
        discount = prod.get('discount')
        prev_price = int(discount.get('prevPrice') / 100) if discount else 0
        title = clean(prod.get('name'))
        description = clean(prod.get('descr')) if prod.get('descr') else ''
        measure_unit = prod.get('measureUnit')
        measure = measure_unit.get('name') if measure_unit else ''
        mercant_short_name = f'mgm_e-{CITY_POSTFIX[self.city]}'
        return {
            'mercant_id': MERCANTS[mercant_short_name],
            'mercant_name': mercant_short_name,
            'product_id': f'{self.city}_{prod.get("itemId")}',
            'id': str(prod.get('itemId')),
            'title': title,
            'description': description,
            'url': '',
            'url_picture': prod.get('mainImg'),
            'time_scrap': datetime.datetime.now().isoformat(),
            'sub_category': cat_tpl[1],
            'category_full_path': f'{cat_tpl[2]}/{cat_tpl[1]}',
            'brand': '',
            'cost': str(int(prod.get('price') / 100)),
            'prev_cost': str(prev_price),
            'measure': measure,
            'city': self.city,
        }

    def upload_results(self):
        """
        Upload scraped product data to the database and update category scrap counts.
        """
        print(f'Magnum express - получено {len(self.results)} sku')
        upload_to_db(
            self.results,
            DB_PATH,
            DB_ROW_DATA_TABLE,
            DB_ROW_DATA_CREATE_STR,
            'product_id'
        )
        update_category_mgm_air(self.category_update, DB_PATH, DB_MGM_E_CATEGORY_TABLE, 'id')
        parent_set = {i[3] for i in self.category_list}
        for par_id in parent_set:
            filter_tpl = ('parent_id', par_id)
            update_parent_category_mgm_air(db_path=DB_PATH, table_name=DB_MGM_E_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl)

    def start(self):
        self.ensure_category_table()
        self.fetch_category_data()
        self.upload_results()


def fast_category_scraper():
    """
    Run the scraper for a fast (limited) set of categories.
    """
    fast_category = '3301, 3302, 3303, 3304'  # Овощи, фрукты, ягоды, зелень, грибы
    scraper = MagnumExpressScraper(fast_category_id=fast_category)
    scraper.start()


def main():
    scraper = MagnumExpressScraper()
    scraper.start()


if __name__ == '__main__':
    main() 