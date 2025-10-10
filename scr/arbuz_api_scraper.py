from typing import Any, Dict, List, Optional
import datetime
import sys
from scr.arbuz_fetchs import PARAMS, URL_NXT, URL_FST, PAGE, SUB_CATALOG, LOUNCH_LIMIT, CITY, HREF, FAST_CATEGORIES_ABZ
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, get_next_categoy_abz
from constants.constants import DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, MERCANTS, DB_ABZ_CATEGORY_CREATE_STR, DB_ABZ_CATEGORY_TABLE, CITY_POSTFIX
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="get scr data")
    parser.add_argument("--limit", type=int, default=1, help="limit of lounching script")
    parser.add_argument("--city", type=str, default='almaty', help="city name")
    return parser.parse_args()


def clean_string(text: Optional[str]) -> str:
    """Remove unwanted characters from a string."""
    if not text:
        return ''
    for ch in ['«', '»', '"', "'"]:
        text = text.replace(ch, '')
    return text


def build_product_dict(product: Dict[str, Any], sub_category: str, category_full_path: str, city: str) -> Dict[str, Any]:
    """Build a product dictionary for upload."""
    title = clean_string(product.get('name'))
    description = clean_string(product.get('description'))
    brand = clean_string(product.get('brandName'))
    mercant_short_name = 'abz' + '-' + CITY_POSTFIX[city]
    return {
        'mercant_id': MERCANTS[mercant_short_name],
        'mercant_name': mercant_short_name,
        'product_id': str(city + '_' + str(product['id'])),
        'id': str(product['id']),
        'title': title,
        'description': description,
        'url': f"https://arbuz.kz{product['uri']}",
        'url_picture': product['image'],
        'time_scrap': str(datetime.datetime.now().isoformat()),
        'sub_category': sub_category,
        'category_full_path': category_full_path,
        'brand': brand,
        'cost': product['priceActual'],
        'prev_cost': product['pricePrevious'],
        'measure': product['measure'],
        'city': city,
    }


class ArbuzApiScraper:
    """
    Scraper for Arbuz API categories and products.
    """
    def __init__(self, catalog_number: str, catalog_href: str, city: str) -> None:
        self.rezult: List[Dict[str, Any]] = []
        self.catalog_number: str = catalog_number
        self.catalog_href: str = catalog_href.replace(CITY, city)
        self.city: str = city
        self.df = None
        self.date_time_now: datetime.datetime = datetime.datetime.now()

    def fill_rezult(self) -> None:
        """
        Fill the result list with product data from all sub-catalogs and pages.
        """
        url = URL_FST.replace(SUB_CATALOG, self.catalog_number)
        PARAMS['referrer'] = PARAMS['referrer'].replace(HREF, self.catalog_href)
        fst_fetch = get_fetch(url, PARAMS)
        category, parent_name = self._get_category_names(fst_fetch)
        sub_catalog_list = self._get_sub_catalog_list(fst_fetch)
        for sub_catalog_dict in sub_catalog_list:
            self._process_sub_catalog(sub_catalog_dict, parent_name, category)

    def _get_category_names(self, fst_fetch: Any):
        try:
            category = fst_fetch.json()['data']['name']
        except Exception:
            category = '<-- нет категории -->'
            print(f'Не удалось получить значение категории для каталога #{self.catalog_number}')
        try:
            parent_name = fst_fetch.json()['data']['parent']['data']['name']
        except Exception:
            parent_name = '<-- нет родительской категории -->'
            print(f'Не удалось получить значение родительской категории')
        return category, parent_name

    def _get_sub_catalog_list(self, fst_fetch: Any) -> List[Dict[str, Any]]:
        return [
            {'id': catalog['id'], 'uri': catalog['uri']}
            for catalog in fst_fetch.json()['data']['catalogs']['data']
        ]

    def _process_sub_catalog(self, sub_catalog_dict: Dict[str, Any], parent_name: str, category: str) -> None:
        url = URL_FST.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
        cur_fetch = get_fetch(url, PARAMS)
        products_count, list_lim = self._get_products_count_and_limit(cur_fetch)
        page_count = self._get_page_count(products_count, list_lim)
        for page_num in range(1, page_count + 1):
            cur_fetch = self._get_page_fetch(sub_catalog_dict, page_num, cur_fetch)
            sub_category, products = self._get_sub_category_and_products(cur_fetch, page_num, page_count)
            category_full_path = parent_name + '/' + category + '/' + sub_category
            print(f'Arbuz {self.city} - запрос {page_num} из {page_count} по {category_full_path}')
            for product in products:
                self.rezult.append(build_product_dict(product, sub_category, category_full_path, self.city))
            if page_num != page_count:
                rand_pause()
        rand_pause()

    def _get_products_count_and_limit(self, cur_fetch: Any):
        products_count = cur_fetch.json()['data']['products']['page']['count']
        list_lim = cur_fetch.json()['data']['products']['page']['limit']
        return products_count, list_lim

    def _get_page_count(self, products_count: int, list_lim: int) -> int:
        add_page = 1 if (products_count % list_lim) > 0 else 0
        return products_count // list_lim + add_page

    def _get_page_fetch(self, sub_catalog_dict: Dict[str, Any], page_num: int, cur_fetch: Any) -> Any:
        if page_num > 1:
            url = URL_NXT.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
            url = url.replace(PAGE, str(page_num))
            cur_fetch = get_fetch(url, PARAMS)
        return cur_fetch

    def _get_sub_category_and_products(self, cur_fetch: Any, page_num: int, page_count: int):
        try:
            sub_category = cur_fetch.json()['data']['name']
        except Exception:
            sub_category = '<-- нет подкатегории -->'
            print(f'Не удалось получить значение sub_category {page_num} из {page_count}')
        try:
            products = cur_fetch.json()['data']['products']['data']
        except Exception:
            products = []
            print(f'Не удалось получить значение products {page_num} из {page_count}')
        return sub_category, products

    def __upload_to_db(self) -> None:
        """
        Upload the scraped product data to the database.
        """
        print(f'Arbuz {self.city} - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')

    def start(self) -> None:
        """
        Start the scraping process: fill results and upload to DB.
        """
        self.fill_rezult()
        self.__upload_to_db()


def fast_category_scraper(city: str) -> None:
    """
    Run the scraper for a predefined list of fast categories for a given city.
    """
    print(f'Run for city - {city}')
    for fast_category in FAST_CATEGORIES_ABZ:
        arbuz = ArbuzApiScraper(
            catalog_number=fast_category['catalog'],
            catalog_href=fast_category['href'],
            city=city
        )
        arbuz.start()


def main() -> None:
    """
    Main entry point for the Arbuz scraper.
    """
    args = parse_args()
    # city = (sys.argv[1] if len(sys.argv) > 1 else 'almaty')
    city = (args.city if args.city else 'almaty')
    print(f'Run for city - {city}')
    # for i in range(LOUNCH_LIMIT):
    for i in range(args.limit):
        print(f'Запуск #{i + 1}')
        next_caterory_dct = get_next_categoy_abz(
            db_path=DB_PATH,
            table_name=DB_ABZ_CATEGORY_TABLE,
            table_create_str=DB_ABZ_CATEGORY_CREATE_STR,
            pk_column='href',
            city=city
        )
        arbuz = ArbuzApiScraper(
            catalog_number=next_caterory_dct['catalog'],
            catalog_href=next_caterory_dct['href'],
            city=city
        )
        arbuz.start()


if __name__ == '__main__':
    main() 