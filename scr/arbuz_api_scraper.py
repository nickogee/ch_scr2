from scr.arbuz_fetchs import PARAMS, URL_NXT, URL_FST, PAGE, SUB_CATALOG, LOUNCH_LIMIT
import datetime
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, get_next_categoy_abz
from constants.constants import DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, MERCANTS,\
                                DB_ABZ_CATEGORY_CREATE_STR, DB_ABZ_CATEGORY_TABLE


class ArbuzApiScraper():

    def __init__(self, catalog_number:str):
        self.rezult = []
        self.catalog_number = catalog_number
        self.df = None
        self.date_time_now = datetime.datetime.now()


    def fill_rezult(self):

        url = URL_FST.replace(SUB_CATALOG, self.catalog_number)
        fst_fetch = get_fetch(url, PARAMS)
        try:
            category = fst_fetch.json()['data']['name']
        except Exception:
            parent_name = '<-- нет категории -->'
            print(f'Не удалось получить значение категории' )

        try:
            parent_name = fst_fetch.json()['data']['parent']['data']['name']
        except Exception:
            parent_name = '<-- нет родительской категории -->'
            print(f'Не удалось получить значение родительской категории' )
        
        sub_catalog_list = [{'id': catalog['id'], 'uri': catalog['uri']}
                            for catalog in fst_fetch.json()['data']['catalogs']['data']]

        for sub_catalog_dict in sub_catalog_list:

            url = URL_FST.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
            cur_fetch = get_fetch(url, PARAMS)

            products_count = cur_fetch.json()['data']['products']['page']['count']
            list_lim = cur_fetch.json()['data']['products']['page']['limit']
            add_page = 1 if (products_count % list_lim) > 0 else 0
            page_count = products_count // list_lim + add_page

            for page_num in range(1, page_count + 1):

                # ответ на запрос для первой страницы уже получен,
                if page_num > 1:
                    url = URL_NXT.replace(SUB_CATALOG, str(sub_catalog_dict['id']))
                    url = url.replace(PAGE, str(page_num))
                    cur_fetch = get_fetch(url, PARAMS)

                try:
                    sub_category = cur_fetch.json()['data']['name']
                except Exception:
                    print(f'Не удалось получить значение sub_category {page_num} из {page_count}' )

                try:
                    products = cur_fetch.json()['data']['products']['data']
                except Exception:
                    print(f'Не удалось получить значение products {page_num} из {page_count}' )
                    continue


                category_full_path = parent_name + '/' + category + '/' + sub_category
                print(f'Arbuz - запрос {page_num} из {page_count} по {category_full_path}')

                for product in products:

                    title = product['name']
                    title = title.replace('«', '')
                    title = title.replace('»', '')
                    title = title.replace('"', '')
                    title = title.replace("'", '')
                    
                    description = product['description']
                    if description:
                        description = description.replace('«', '')
                        description = description.replace('»', '')
                        description = description.replace('"', '')
                        description = description.replace("'", '')
                    else:
                        description = ''
                    
                    brand = product['brandName']
                    if brand:
                        brand = brand.replace('«', '')
                        brand = brand.replace('»', '')
                        brand = brand.replace('"', '')
                        brand = brand.replace("'", '')
                    else:
                        brand = ''

                    l = {
                        'mercant_id': MERCANTS['abz'],
                        'mercant_name': 'abz',
                        'product_id': str(product['id']),
                        'title':  title,
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
                    }

                    self.rezult.append(l)

                if page_num != page_count:
                    rand_pause()

            rand_pause()

    def __upload_to_db(self):
        print(f'Arbuz - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')


    def start(self):
        self.fill_rezult()
        self.__upload_to_db()


def fast_category_scraper():
    
    # Свежие Овощи и фрукты
    fast_category_ls = ['225177', '225178', '225176', '225569', '225562', '225444', '225445', '249886', '225189']
    for fast_category in fast_category_ls:
   
        arbuz = ArbuzApiScraper(fast_category)
        arbuz.start()


def main():

    for i in range(LOUNCH_LIMIT):

        print(f'Запуск #{i + 1}')
        next_caterory_dct = get_next_categoy_abz(DB_PATH, DB_ABZ_CATEGORY_TABLE, DB_ABZ_CATEGORY_CREATE_STR, 'href')

        arbuz = ArbuzApiScraper(next_caterory_dct['catalog'])
        arbuz.start()



if __name__ == '__main__':
    main()




