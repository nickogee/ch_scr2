import datetime
import sys
from scr.klever_fetch import URL_CATEGORY, PARAMS_CATEGORY, REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_kvr
from constants.constants import DB_PATH, DB_KVR_CATEGORY_TABLE, DB_KVR_CATEGORY_CREATE_STR, MERCANTS, \
    DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX


class KleverScraper:
    """
    Scraper for Klever API. Handles category and product data extraction and database upload.
    """
    def __init__(self, city, fast_category_ls=None):
        self.city = city
        self.fast_category_ls = fast_category_ls
        self.limit_off = bool(fast_category_ls)
        self.category_list = []
        self.category_update = []
        self.results = []
        self.date_time_now = datetime.datetime.now()

    def ensure_category_table(self):
        """
        Ensure the category table exists and is populated with current data.
        """
        if table_exists(db_path=DB_PATH, table_name=DB_KVR_CATEGORY_TABLE):
            return
        response = get_fetch(url=URL_CATEGORY, params=PARAMS_CATEGORY)
        categories = response.json().get('content', [])
        for cat in categories:
            if cat.get('status') != 'ACTIVE':
                continue
            category = {
                'id': str(cat.get('id')),
                'name': cat.get('name'),
                'city': self.city,
            }
            print(f"- Получаем категорию id={cat['id']}, name={cat['name']}")
            self.category_list.append(category)
        if self.category_list:
            upload_to_db(
                rezult=self.category_list,
                db_path=DB_PATH,
                table_name=DB_KVR_CATEGORY_TABLE,
                table_create_str=DB_KVR_CATEGORY_CREATE_STR,
                pk_column='id'
            )

    def fetch_category_data(self):
        """
        Fetch product data for each category and store results in self.results.
        """
        self.category_list = get_next_categoy_kvr(
            db_path=DB_PATH,
            table_name=DB_KVR_CATEGORY_TABLE,
            pk_column='id',
            fast_category_ls=self.fast_category_ls,
            city=self.city
        )
        req_cnt = 0
        if not self.category_list:
            return
        for cat in self.category_list:
            if not self.limit_off and req_cnt > REQ_LIMIT:
                break
            catalog_id = cat['id']
            page = 1
            while True:
                params = PARAMS_CATALOG.copy()
                params['params']['CatalogId'] = str(catalog_id)
                params['params']['pageNumber'] = str(page)
                response = get_fetch(url=URL_CATALOG, params=params)
                req_cnt += 1
                page += 1
                if response.status_code != 200:
                    break
                content = response.json().get('content')
                if not content:
                    break
                for prod in content:
                    self.results.append(self._parse_product(prod, cat))
                print(f'Klever {self.city} - страница {page - 1} категории {cat["name"]} запрос {req_cnt}')
                rand_pause()
            # After finishing all pages for a category, mark it for update
            self.category_update.append({
                'id': cat['id'],
                'scrap_count': cat.get('scrap_count', 0) + 1
            })

    def _parse_product(self, prod, cat):
        """
        Parse a single product dictionary into the database row format.
        """
        def clean(text):
            if not text:
                return ''
            return text.replace('«', '').replace('»', '').replace('"', '').replace("'", '')
        title = clean(prod.get('name'))
        images = prod.get('images')
        image = images[0]['path'] if images else ''
        sub_category_name = prod.get('categoryName')
        category_full_path = f'{cat["name"]}/{sub_category_name}/' if sub_category_name else f'{cat["name"]}/'
        discount_percent = prod.get('discountPercent')
        actual_cost = prod.get('discountPrice')
        prev_cost = prod.get('retailPrice') if discount_percent else 0
        brand = clean(str(prod.get('brandName')))
        mercant_short_name = f'kvr-{CITY_POSTFIX[self.city]}'
        return {
            'mercant_id': MERCANTS[mercant_short_name],
            'mercant_name': mercant_short_name,
            'product_id': f'{self.city}_{prod.get("id")}',
            'id': str(prod.get('id')),
            'title': title,
            'description': '',
            'url': '',  # No product card URL available
            'url_picture': str(image),
            'time_scrap': datetime.datetime.now().isoformat(),
            'sub_category': sub_category_name,
            'category_full_path': category_full_path,
            'brand': brand,
            'cost': str(actual_cost),
            'prev_cost': str(prev_cost),
            'measure': prod.get('measureName'),
            'city': self.city,
        }

    def upload_results(self):
        """
        Upload scraped product data to the database.
        """
        print(f'Klever - получено {len(self.results)} sku')
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


def fast_category_scraper(city):
    """
    Run the scraper for a fast (limited) set of categories.
    """
    fast_category_ls = [
        '1088',  # Овощи-фрукты
    ]
    scraper = KleverScraper(city=city, fast_category_ls=fast_category_ls)
    scraper.start()


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else 'astana'
    print(f'Run for city - {city}')
    scraper = KleverScraper(city)
    scraper.start()


if __name__ == '__main__':
    main() 