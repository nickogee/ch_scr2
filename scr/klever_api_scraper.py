from scr.klever_fetch import URL_CATEGORY, PARAMS_CATEGORY, \
                                REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
import datetime
import sys
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_kvr
from constants.constants import DB_PATH, DB_KVR_CATEGORY_TABLE, DB_KVR_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX


class KleverScrapper():
    def __init__(self, city, fast_category_ls=None) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.fast_category_ls = fast_category_ls
        self.limit_off = bool(fast_category_ls)
        self.city = city
    
    def fill_category_table(self):
        '''Создает и перезаполняет актуальными данными таблицу категорий, если она не существует'''

        if not table_exists(db_path=DB_PATH, table_name=DB_KVR_CATEGORY_TABLE):
            
            resp = get_fetch(url=URL_CATEGORY, params=PARAMS_CATEGORY)
            resp_js = resp.json()
            content = resp_js['content']

            for cat_dct in content:
                if cat_dct['status'] != 'ACTIVE':
                    continue
                
                # добавляем категорию первого уровня
                dct = {
                        'id': str(cat_dct.get('id')),
                        'name': cat_dct.get('name'),
                        'city': self.city,
                        }

                print(f"- Получаем категорию id={cat_dct['id']}, name={cat_dct['name']}")
                self.category_list.append(dct)

            if self.category_list:
                upload_to_db(rezult=self.category_list, 
                            db_path=DB_PATH, 
                            table_name=DB_KVR_CATEGORY_TABLE,
                            table_create_str=DB_KVR_CATEGORY_CREATE_STR,
                            pk_column='id')

    def fill_category_data(self):
        '''Парсит данные по нужным категориям'''

        self.category_list = get_next_categoy_kvr(db_path=DB_PATH, table_name=DB_KVR_CATEGORY_TABLE, 
                                                  pk_column='id', fast_category_ls=self.fast_category_ls, city=self.city)
        
        # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
        req_cnt = 0
        if self.category_list:
            for cat_dct in self.category_list:

                if (not self.limit_off) and (req_cnt > REQ_LIMIT):
                    break
                
                # текущая категория 
                catalog_di = cat_dct['id']

                # условие выхода из цикла: текущая страница - последняя
                is_last_page = False

                # текущая страница
                page = 1

                while not is_last_page:

                    params = PARAMS_CATALOG.copy()
                    params['params']['CatalogId'] = str(catalog_di)
                    params['params']['pageNumber'] = str(page)
                    
                    resp = get_fetch(url=URL_CATALOG, params=params)
                    
                    req_cnt += 1
                    page += 1

                    if resp.status_code == 200:
                        resp_js = resp.json()
                        content_ls = resp_js.get('content')

                        if content_ls:
                        
                            for prod_dct in content_ls:

                                title = prod_dct.get('name')
                                title = title.replace('«', '')
                                title = title.replace('»', '')
                                title = title.replace('"', '')
                                title = title.replace("'", '')
                            
                                description = ''

                                images_ls = prod_dct.get('images')
                                if images_ls:
                                    image = images_ls[0]['path']
                                else:
                                    image = ''

                                sub_category_name = prod_dct.get('categoryName')
                                if sub_category_name:
                                    category_full_path = f'{cat_dct["name"]}/{sub_category_name}/'
                                else:
                                    category_full_path = f'{cat_dct["name"]}/'


                                
                                discountPercent = prod_dct.get('discountPercent')
                                actual_cost = prod_dct.get('discountPrice')

                                if discountPercent:
                                    prev_cost = prod_dct.get('retailPrice')
                                else:
                                    prev_cost = 0
                                

                                brand = str(prod_dct.get('brandName'))
                                if brand:
                                    brand = brand.replace('«', '')
                                    brand = brand.replace('»', '')
                                    brand = brand.replace('"', '')
                                    brand = brand.replace("'", '')
                                else:
                                    brand = ''

                                mercant_short_name = 'kvr' + '-' + CITY_POSTFIX[self.city]

                                l = {
                                'mercant_id': MERCANTS[mercant_short_name],
                                'mercant_name': mercant_short_name,
                                'product_id': str(self.city + '_' + prod_dct.get('id')),
                                'id': str(prod_dct.get('id')),
                                'title': title,
                                'description': description,
                                'url': '', # здесь отсутствует url товара (карточки товара)
                                'url_picture': str(image),
                                'time_scrap': str(datetime.datetime.now().isoformat()),
                                'sub_category': sub_category_name,
                                'category_full_path': category_full_path,
                                'brand': brand,
                                'cost': str(actual_cost),
                                'prev_cost': str(prev_cost),
                                'measure': prod_dct.get('measureName'),
                                'city': self.city,
                                    }

                                self.rezult.append(l) 

                        else:
                            is_last_page = True

                    print(f'Klever {self.city} - страница {page - 1} категории {cat_dct["name"]} запрос {req_cnt}')
                    rand_pause()

            else:
                # Кочились страницы категории. Добавим категорию в список для обновления scrap_count
                d = {
                    'id': cat_dct['id'],
                    'scrap_count': cat_dct['scrap_count'] + 1 
                    }
                self.category_update.append(d)

    def __upload_to_db(self):
        
        # грузим "спарсенные" данные в базу
        print(f'Klever - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')
        

    def start(self):
        self.fill_category_table()
        self.fill_category_data()
        self.__upload_to_db()


def fast_category_scraper(city):

    fast_category_ls = [
        '1088', # Овощи-фрукты
    ]

    klever = KleverScrapper(city=city, fast_category_ls=fast_category_ls)
    klever.start()    


def main():
    city = (sys.argv[1] if len(sys.argv) > 1 else 'astana')
    print(f'Run for city - {city}')
    klever = KleverScrapper(city)
    klever.start()


if __name__ == '__main__':
    main()


