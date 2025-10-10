import datetime
import sys
from scr.magnum_fetchs import PARAMS_TOKEN, URL_TOKEN, URL_CATEGORY, PARAMS_CATEGORY, \
    REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG, CITYS_PLATFORM_ID
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm_air, \
    update_category_mgm_air, update_parent_category_mgm
from constants.constants import DB_PATH, DB_MGM_CATEGORY_TABLE, DB_MGM_CATEGORY_CREATE_STR, MERCANTS, \
    DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="get mgm data")
    parser.add_argument("--limit", type=int, default=1, help="limit of lounching script")
    return parser.parse_args()



class MagnumScraper:
    """
    Scraper for Magnum API. Handles category and product data extraction and database upload.
    """
    def __init__(self, city, fast_category_id=None):
        self.city = city
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
        if table_exists(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE):
            return
        for cur_city, cur_platform_id in CITYS_PLATFORM_ID.items():
            params_head = PARAMS_CATEGORY.copy()
            params_head['params']['parentId'] = ''
            params_head['headers']['Authorization'] = self.token
            params_head['params']['platformId'] = cur_platform_id
            resp = get_fetch(url=URL_CATEGORY, params=params_head)
            resp_js = resp.json()
            for head_cat in resp_js:
                if head_cat['id'] in (60, 70):  # Skip discount and Kurban-Ait categories
                    continue
                self.category_list.append(self._make_category_dict(head_cat, cur_city, '1', ''))
                print(f"Получаем категорию 1 уровня city= {cur_city} id={head_cat['id']}, name={head_cat['name']}")
                for chld_cat in head_cat.get('childCategories', []):
                    self.category_list.append(self._make_category_dict(chld_cat, cur_city, '2', chld_cat['parentId']))
                    print(f"Получаем категорию 2 уровня city= {cur_city} id={chld_cat['id']}, name={chld_cat['name']}")
                    rand_pause()
                    # Fetch 3rd level categories
                    params_chld = PARAMS_CATEGORY.copy()
                    params_chld['params']['parentId'] = str(chld_cat['parentId'])
                    params_chld['headers']['Authorization'] = self.token
                    params_chld['params']['platformId'] = cur_platform_id
                    chld_resp = get_fetch(url=URL_CATEGORY, params=params_chld)
                    chld_resp_js = chld_resp.json()
                    for i in chld_resp_js:
                        for sub_chld_cat in i.get('childCategories', []):
                            self.category_list.append(self._make_category_dict(sub_chld_cat, cur_city, '3', sub_chld_cat['parentId']))
                            print(f"Получаем категорию 3 уровня city={cur_city} id={sub_chld_cat['id']}, name={sub_chld_cat['name']}")
        if self.category_list:
            upload_to_db(
                rezult=self.category_list,
                db_path=DB_PATH,
                table_name=DB_MGM_CATEGORY_TABLE,
                table_create_str=DB_MGM_CATEGORY_CREATE_STR,
                pk_column='key_column'
            )

    def _make_category_dict(self, cat, city, lvl, parent_id):
        return {
            'parent_id': str(parent_id) if parent_id else str(cat.get('parentId', '')),
            'id': str(cat['id']),
            'name': str(cat['name']),
            'category_lvl': lvl,
            'city': city,
            'key_column': f"{city}/{cat['id']}",
        }

    def fetch_category_data(self):
        """
        Fetch product data for each category and store results in self.results.
        """
        self.category_list = get_next_categoy_list_mgm_air(
            db_path=DB_PATH,
            table_name=DB_MGM_CATEGORY_TABLE,
            mercant='mgm',
            cat_lvl='2',
            fast_category_id=self.fast_category_id,
            city=self.city
        )
        req_cnt = 0
        for cat_tpl in self.category_list:
            if not self.limit_off and req_cnt > REQ_LIMIT:
                break
            if cat_tpl[9] != self.city:
                continue
            for page in range(21):
                params = PARAMS_CATALOG.copy()
                params['params']['categoryIds'] = cat_tpl[0]
                params['params']['pageId'] = str(page)
                params['headers']['Authorization'] = self.token
                params['params']['platformId'] = CITYS_PLATFORM_ID[self.city]
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
                        'key_column': f"{self.city}/{cat_tpl[0]}",
                        'scrap_count': cat_tpl[4] + 1
                    })
                    break
                print(f'Magnum {self.city} - страница {page + 1} категории "{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}" запрос {req_cnt}')
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
        mercant_short_name = f'mgm-{CITY_POSTFIX[self.city]}'
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
            'category_full_path': f'{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}',
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
        print(f'Magnum - получено {len(self.results)} sku')
        upload_to_db(
            self.results,
            DB_PATH,
            DB_ROW_DATA_TABLE,
            DB_ROW_DATA_CREATE_STR,
            'product_id'
        )
        update_category_mgm_air(self.category_update, DB_PATH, DB_MGM_CATEGORY_TABLE, 'key_column')
        # Update parent categories' scrap_count
        parent_set_lvl2 = {i[6] for i in self.category_list}
        for par_id in parent_set_lvl2:
            filter_ls = [('parent_id', par_id), ('city', self.city)]
            update_parent_category_mgm(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE, pk_column='key_column', filter_ls=filter_ls)
        parent_set_lvl1 = {i[7] for i in self.category_list}
        for par_id in parent_set_lvl1:
            filter_ls = [('parent_id', par_id), ('city', self.city)]
            update_parent_category_mgm(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE, pk_column='key_column', filter_ls=filter_ls)

    def start(self):
        self.ensure_category_table()
        self.fetch_category_data()
        self.upload_results()


def fast_category_scraper(city):
    """
    Run the scraper for a fast (limited) set of categories.
    """
    fast_category = '1103'  # Овощи, фрукты, ягоды, зелень, грибы
    print(f'Run for city - {city}')
    scraper = MagnumScraper(city=city, fast_category_id=fast_category)
    scraper.start()


def main():
    args = parse_args()
    city = sys.argv[1] if len(sys.argv) > 1 else 'astana'
    print(f'Run for city - {city}')
    for i in range(args.limit):
        print(f'Запуск #{i + 1}')
        scraper = MagnumScraper(city=city)
        scraper.start()


if __name__ == '__main__':
    main() 