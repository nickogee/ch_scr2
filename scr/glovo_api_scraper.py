from typing import Any, Dict, List, Optional
import datetime
from scr.glovo_fetchs import PARAMS, URL_SERV
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, get_next_categoy_glv, get_fast_category_glv, update_category_glv
from constants.constants import DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, MERCANTS, DB_GLV_CATEGORY_TABLE, DB_GLV_CATEGORY_CREATE_STR, CITY_POSTFIX


def clean_string(text: Optional[str]) -> str:
    """Remove unwanted characters from a string."""
    if not text:
        return ''
    for ch in ['«', '»', '"', "'"]:
        text = text.replace(ch, '')
    return text


def build_product_dict(product: Dict[str, Any], sub_category_name: str, category_full_path: str, city: str, category_url: str) -> Dict[str, Any]:
    """Build a product dictionary for upload."""
    data = product.get('data', {})
    title = clean_string(data.get('name'))
    imageUrl = data.get('imageUrl', '')
    url_picture = imageUrl if imageUrl else ''
    prev_price = data.get('price', 0)
    promotion = data.get('promotion')
    price = promotion.get('price') if promotion else 0
    mercant_short_name = 'glv' + '-' + CITY_POSTFIX[city]
    return {
        'mercant_id': MERCANTS[mercant_short_name],
        'mercant_name': mercant_short_name,
        'product_id': str(city + '_' + str(data.get('id'))),
        'id': str(data.get('id')),
        'title': title,
        'description': '',
        'url': f'https://glovoapp.com/kz/ru/almaty/glovo-express-ala/?content={category_url}',
        'url_picture': url_picture,
        'time_scrap': str(datetime.datetime.now().isoformat()),
        'sub_category': sub_category_name,
        'category_full_path': category_full_path,
        'brand': '',
        'cost': price if price else prev_price,
        'prev_cost': prev_price if price else 0,
        'measure': '',
        'city': city,
    }


class GlovoApiScraper:
    """
    Scraper for Glovo API categories and products.
    """
    def __init__(self, cat_ls: Dict[str, Any]) -> None:
        self.rezult: List[Dict[str, Any]] = []
        self.df = None
        self.date_time_now: datetime.datetime = datetime.datetime.now()
        self.city: str = 'almaty'
        self.categories: List[Dict[str, Any]] = cat_ls

    def _extract_categories(self, head_response: Any, cat_dct: Dict[str, Any]) -> List[Dict[str, Any]]:
        head_resp_json = head_response.json()
        data = head_resp_json.get('data')
        if data:
            body = data.get('body')
            if body and len(body) > 0:
                body_data = body[0].get('data')
                if body_data:
                    return body_data['elements']
                else:
                    print('Не найден элемент "elements"')
            else:
                print('Не найден элемент "body" или не пустой')
        else:
            title = cat_dct['title']
            slug = cat_dct['slug']
            print(f'Не найден элемент "data" для категории {title} ({slug})')
        return []

    def fill_rezult(self) -> None:
        """
        Populate the result list with product data from all categories and subcategories.
        """
        for curr_category in self.categories:
            category_name = curr_category['title']
            parent_category_name = curr_category['parent']
            try:
                response = get_fetch(f"{URL_SERV}{curr_category['path']}", PARAMS)
                response_json = response.json()
                response_data = response_json.get('data', {})
                category_url = response_data.get('activeElementSlug', '')
                category_groups = response_data.get('body', [])
                if not category_groups:
                    print(f'Нет данных по подкатегориям для {category_name}')
                    continue
                self._process_category_groups(category_groups, category_name, category_url, parent_category_name)
            except Exception as ex:
                print(f"Ошибка при обработке категории '{category_name}': {ex}")
                continue
            finally:
                rand_pause()

            curr_category['scrap_count'] += 1

    def _process_category_groups(self, category_groups: List[Dict[str, Any]], category_name: str, category_url: str, parent_category_name: str) -> None:
        page_num = 1
        for sub_cat in category_groups:
            sub_category_name = sub_cat['data'].get('title')
            products = sub_cat['data'].get('elements')
            if not products:
                continue
            category_full_path = parent_category_name + '/' + category_name + '/' + sub_category_name
            print(f'Glovo - запрос {page_num} из {len(category_groups)} по {category_full_path}')
            for product in products:
                self.rezult.append(build_product_dict(product, sub_category_name, category_full_path, self.city, category_url))
            page_num += 1

    def __upload_to_db(self) -> None:
        """
        Upload the scraped product data to the database.
        """
        print(f'Glovo {self.city} - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')

        # обновляем scrap_count для "спарсеных" категорий 2-го уровня
        update_category_glv(self.categories, DB_PATH, DB_GLV_CATEGORY_TABLE, 'id')


    def start(self) -> None:
        """
        Start the scraping process: fill results and upload to DB.
        """
        self.fill_rezult()
        self.__upload_to_db()


def fast_category_scraper() -> None:
    """
    Run the scraper for a predefined fast category (Fruits and Vegetables).
    """
    fast_category_ls = get_fast_category_glv(DB_PATH, DB_GLV_CATEGORY_TABLE, DB_GLV_CATEGORY_CREATE_STR, 'id')
    glovo = GlovoApiScraper(fast_category_ls)
    glovo.start()


def main() -> None:
    """
    Main entry point for the Glovo scraper.
    """
    next_caterory_ls = get_next_categoy_glv(DB_PATH, DB_GLV_CATEGORY_TABLE, DB_GLV_CATEGORY_CREATE_STR, 'id')
    glovo = GlovoApiScraper(next_caterory_ls)
    glovo.start()


if __name__ == '__main__':
    main() 