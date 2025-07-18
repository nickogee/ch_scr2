import datetime
import random
from scr.volt_fetchs import (
    PARAMS_TOKEN, URL_TOKEN, REFRESH_TOKEN_MASK,
    URL_CATEGORY, PARAMS_CATEGORY, CURRENT_CATEGORY_MASK, URL_CATALOG, PARAMS_CATALOG
)
from scr.share_functions import get_fetch, format_name
from scr.database_worker import (
    upload_to_db, table_exists, get_next_categoy_vlt,
    get_data_from, truncate_table, create_table
)
from constants.constants import (
    DB_PATH, DB_VLT_CATEGORY_TABLE, DB_VLT_CATEGORY_CREATE_STR, MERCANTS, CITY_POSTFIX,
    DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, DB_VLT_REFRESH_TOKEN_TABLE, DB_VLT_REFRESH_TOKEN_CREATE_STR
)

class VoltScraper:
    """
    Scraper for Volt API. Handles category and product data extraction and database upload.
    """
    def __init__(self, fast_category_ls=None):
        self.date_time_now = datetime.datetime.now()
        self.results = []
        self.category_list = []
        self.category_update = []
        self.fast_category_ls = fast_category_ls
        self.refresh_token = None
        self.userlocationlng = f'76.{random.randint(889433, 960513)}'
        self.userlocationlat = f'43.2{random.randint(32015, 49646)}'
        self.token = None
        self.city = 'almaty'
        self.create_refresh_token_table()

    def create_refresh_token_table(self):
        create_table(
            db_path=DB_PATH,
            table_name=DB_VLT_REFRESH_TOKEN_TABLE,
            table_create_str=DB_VLT_REFRESH_TOKEN_CREATE_STR
        )

    def get_token(self):
        if not self.refresh_token:
            result = get_data_from(
                db_path=DB_PATH,
                table_name=DB_VLT_REFRESH_TOKEN_TABLE,
                columns='refresh_token',
                filter_tpl=tuple()
            )
            if isinstance(result, list) and result:
                self.refresh_token = result[0][0]
        if self.refresh_token and not self.token:
            PARAMS_TOKEN['body'] = PARAMS_TOKEN['body'].replace(REFRESH_TOKEN_MASK, self.refresh_token)
            resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
            resp_js = resp.json()
            if resp_js.get('access_token'):
                self.token = resp_js['access_token']
                done = truncate_table(
                    db_path=DB_PATH,
                    table_name=DB_VLT_REFRESH_TOKEN_TABLE
                )
                if done:
                    upload_to_db(
                        rezult=[{'refresh_token': resp_js['refresh_token']}],
                        db_path=DB_PATH,
                        table_name=DB_VLT_REFRESH_TOKEN_TABLE,
                        table_create_str=DB_VLT_REFRESH_TOKEN_CREATE_STR,
                        pk_column='refresh_token'
                    )

    def ensure_category_table(self):
        """
        Creates and populates the category table with current data if it does not exist.
        """
        if not self.token:
            self.get_token()
        if self.token and not table_exists(db_path=DB_PATH, table_name=DB_VLT_CATEGORY_TABLE):
            params_head = PARAMS_CATEGORY.copy()
            resp = get_fetch(url=URL_CATEGORY, params=params_head)
            resp_js = resp.json()
            category_ls = resp_js.get('categories')
            if category_ls:
                for head_dct in category_ls:
                    if not head_dct.get('parent_category_id'):
                        name = format_name(head_dct.get('name'))
                        dct = {
                            'id': str(head_dct.get('id')),
                            'name': str(name.strip()),
                        }
                        print(f"Получаем категорию id={head_dct['id']}, {name}")
                        self.category_list.append(dct)
                if self.category_list:
                    upload_to_db(
                        rezult=self.category_list,
                        db_path=DB_PATH,
                        table_name=DB_VLT_CATEGORY_TABLE,
                        table_create_str=DB_VLT_CATEGORY_CREATE_STR,
                        pk_column='id'
                    )
        elif not self.token:
            print('Токен отсутствует')

    def fetch_category_data(self):
        """
        Parses and collects product data for the required categories.
        """
        if not self.token:
            print('Токен отсутствует')
            return
        self.category_list = get_next_categoy_vlt(
            db_path=DB_PATH,
            table_name=DB_VLT_CATEGORY_TABLE,
            pk_column='id',
            fast_category_ls=self.fast_category_ls
        )
        for cat_dct in self.category_list:
            params = PARAMS_CATALOG.copy()
            params['headers']['path'] = params['headers']['path'].replace(CURRENT_CATEGORY_MASK, cat_dct['id'])
            params['headers']['Authorization'] = f'Bearer {self.token}'
            params['headers']['userlocationlng'] = self.userlocationlng
            params['headers']['userlocationlat'] = self.userlocationlat
            url = URL_CATALOG.replace(CURRENT_CATEGORY_MASK, cat_dct['id'])
            resp = get_fetch(url=url, params=params)
            resp_js = resp.json()
            categories = resp_js.get('categories')
            content = resp_js.get('items')
            if content:
                sku_count = 0
                for prod_dct in content:
                    title = self._clean_text(prod_dct.get('name'))
                    description = self._clean_text(prod_dct.get('description')) if prod_dct.get('description') else ''
                    category_name, sub_category_name = self._get_category_names(categories, prod_dct.get('category'))
                    if not sub_category_name:
                        sub_category_name = '<empty>'
                        print(f'Не найдена подкатегория для {title}')
                    if not category_name:
                        category_name = '<empty>'
                        print(f'Не найдена родительская категория для {title}')
                    cost, prev_cost = self._get_costs(prod_dct)
                    mercant_short_name = f'vlt-{CITY_POSTFIX[self.city]}'
                    l = {
                        'mercant_id': MERCANTS[mercant_short_name],
                        'mercant_name': mercant_short_name,
                        'product_id': f'{self.city}_{prod_dct.get("id")}',
                        'id': str(prod_dct.get('id')),
                        'title': title,
                        'description': description,
                        'url': '',
                        'url_picture': prod_dct.get('image'),
                        'time_scrap': datetime.datetime.now().isoformat(),
                        'sub_category': sub_category_name,
                        'category_full_path': f'/{category_name}/{sub_category_name}',
                        'brand': '',
                        'cost': cost,
                        'prev_cost': prev_cost,
                        'measure': prod_dct.get('unit_info'),
                        'city': self.city,
                    }
                    sku_count += 1
                    self.results.append(l)
                print(f'Volt {self.city} -  категория "/{category_name}/" товаров {sku_count}')

    def _clean_text(self, text):
        if not text:
            return ''
        return text.replace('«', '').replace('»', '').replace('"', '').replace("'", '')

    def _get_category_names(self, categories, sub_cat_id):
        category_name = None
        sub_category_name = None
        parent_category_id = None
        for cat in categories:
            if cat['id'] == sub_cat_id:
                sub_category_name = format_name(cat['name'])
                parent_category_id = cat['parent_category_id']
                break
        if parent_category_id:
            for parent_cat in categories:
                if parent_cat['id'] == parent_category_id:
                    category_name = format_name(parent_cat['name'])
                    break
        return category_name, sub_category_name

    def _get_costs(self, prod_dct):
        unformatted_unit_price = prod_dct.get('unformatted_unit_price')
        if unformatted_unit_price:
            cost = str(int(unformatted_unit_price.get('price', 0) / 100))
            prev_cost = str(int(unformatted_unit_price.get('original_price', 0) / 100)) if unformatted_unit_price.get('original_price') else '0'
        else:
            cost = str(int(prod_dct.get('baseprice', 0) / 100))
            prev_cost = '0'
        return cost, prev_cost

    def upload_results(self):
        print(f'Volt {self.city} - получено {len(self.results)} sku')
        upload_to_db(
            self.results,
            DB_PATH,
            DB_ROW_DATA_TABLE,
            DB_ROW_DATA_CREATE_STR,
            'product_id'
        )

    def start(self):
        self.ensure_category_table()
        self.fetch_category_data()
        self.upload_results()


def fast_category_scraper():
    fast_category_ls = [
        '73400dc454444536b021ee99',
        'fa11fe7023bb4bd8822ec45d',
    ]
    volt = VoltScraper(fast_category_ls=fast_category_ls)
    volt.start()

def main():
    volt = VoltScraper()
    volt.start()

def initiate():
    volt = VoltScraper()
    volt.create_refresh_token_table()

if __name__ == '__main__':
    main() 