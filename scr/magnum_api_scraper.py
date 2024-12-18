from scr.magnum_fetchs import PARAMS_TOKEN, URL_TOKEN, URL_CATEGORY, PARAMS_CATEGORY, \
                                REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG, CITYS_PLATFORM_ID
import datetime
import sys
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm_air, \
                                update_category_mgm_air, update_parent_category_mgm
from constants.constants import DB_PATH, DB_MGM_CATEGORY_TABLE, DB_MGM_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX


class MagnumScrapper():
    def __init__(self, city, fast_category_id=None) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.fast_category_id = fast_category_id
        self.limit_off = bool(fast_category_id)
        self.token = None
        self.city = city
        self.get_token()
        

    
    def get_token(self):
        if not self.token:
            resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
            resp_js = resp.json()
            
            if resp_js['token']:
                self.token = resp_js['token']
    

    def fill_category_table(self):
        '''Создает и перезаполняет актуальными данными таблицу категорий, если она не существует'''

        if not table_exists(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE):

            for cur_city, cur_platform_id in CITYS_PLATFORM_ID.items():

                # для самого верхнего уровня категорий PARENT_ID пустой
                params_head = PARAMS_CATEGORY.copy()
                params_head['params']['parentId'] = ''
                params_head['headers']['Authorization'] = self.token
                params_head['params']['platformId'] = cur_platform_id
                
                resp = get_fetch(url=URL_CATEGORY, params=params_head)
                resp_js = resp.json()
                
                for head_dct in resp_js:
                    # категория с  id = 60 - это категория "скидки", id = 70 - это "Курбан-Айт"
                    if head_dct['id'] == 60 or head_dct['id'] == 70:
                        continue
                    
                    # добавляем категорию первого уровня
                    dct = {
                        'parent_id': '',
                        'id': str(head_dct['id']),
                        'name': str(head_dct['name']),
                        'category_lvl': '1',
                        'city': cur_city,
                        'key_column': cur_city + '/' + str(head_dct['id']),
                    }

                    print(f"Получаем категорию 1 уровня city= {cur_city} id={head_dct['id']}, name={head_dct['name']}")
                    self.category_list.append(dct)

                    chld_ls = head_dct.get('childCategories')
                    if chld_ls:
                        for chld_dct in chld_ls:
                            
                            # добавляем категорию второго уровня
                            dct = {
                            'parent_id': str(chld_dct['parentId']),
                            'id': str(chld_dct['id']),
                            'name': str(chld_dct['name']),
                            'category_lvl': '2',
                            'city': cur_city,
                            'key_column': cur_city + '/' + str(chld_dct['id']),
                                    }
                            
                            print(f"Получаем категорию 2 уровня city= {cur_city} id={chld_dct['id']}, name={chld_dct['name']}")
                            self.category_list.append(dct)

                            rand_pause()

                            # для каждой категории второго уровня делаем запрос, чтобы получить дочерние категории (3-го уровня)
                            params_chld = PARAMS_CATEGORY.copy()
                            params_chld['params']['parentId'] = str(chld_dct['parentId'])
                            params_chld['headers']['Authorization'] = self.token
                            params_chld['params']['platformId'] = cur_platform_id
                            
                            chld_resp = get_fetch(url=URL_CATEGORY, params=params_chld)
                            chld_resp_js = chld_resp.json()

                            for i in chld_resp_js:
                                # здесь нужны только дочерние элементы
                                sub_chld_ls = i.get('childCategories')
                                if sub_chld_ls:
                                    for sub_chld_dct in sub_chld_ls:
                                        
                                        # добавляем категорию третьего уровня
                                        dct = {
                                        'parent_id': str(sub_chld_dct['parentId']),
                                        'id': str(sub_chld_dct['id']),
                                        'name': str(sub_chld_dct['name']),
                                        'category_lvl': '3',
                                        'city': cur_city,
                                        'key_column': cur_city + '/' + str(sub_chld_dct['id']),
                                                }

                                        print(f"Получаем категорию 3 уровня city={cur_city} id={sub_chld_dct['id']}, name={sub_chld_dct['name']}")
                                        self.category_list.append(dct)

            if self.category_list:
                upload_to_db(rezult=self.category_list, 
                            db_path=DB_PATH, 
                            table_name=DB_MGM_CATEGORY_TABLE,
                            table_create_str=DB_MGM_CATEGORY_CREATE_STR,
                            pk_column='key_column')


    def fill_category_data(self):
        '''Парсит данные по нужным категориям'''

        self.category_list = get_next_categoy_list_mgm_air(db_path=DB_PATH, 
                            table_name=DB_MGM_CATEGORY_TABLE, mercant='mgm', cat_lvl='2', 
                            fast_category_id=self.fast_category_id, city=self.city)
        
        # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
        req_cnt = 0
        for cat_tpl in self.category_list:

            if (not self.limit_off) and (req_cnt > REQ_LIMIT):
                break

            if cat_tpl[9] != self.city:
                continue

            # максимальное количество страниц одной категории 3-го уровня - 20
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

                    for prod_dct in content:                      
                        
                        discount_dct = prod_dct.get('discount')
                        if discount_dct:
                            prev_price = int(discount_dct.get('prevPrice')/100)
                        else:
                            prev_price = 0

                        title = prod_dct.get('name')
                        title = title.replace('«', '')
                        title = title.replace('»', '')
                        title = title.replace('"', '')
                        title = title.replace("'", '')
                        
                        description = prod_dct.get('descr')
                        if description:
                            description = description.replace('«', '')
                            description = description.replace('»', '')
                            description = description.replace('"', '')
                            description = description.replace("'", '')
                        else:
                            description = ''


                        measureUnit = prod_dct.get('measureUnit')
                        if measureUnit:
                            measure = measureUnit.get('name')
                        else:
                            measure = ''

                        mercant_short_name = 'mgm' + '-' + CITY_POSTFIX[self.city]
   
                        l = {
                        'mercant_id': MERCANTS[mercant_short_name],
                        'mercant_name': mercant_short_name,
                        'product_id': str(self.city + '_' + str(prod_dct.get('itemId'))),
                        'id': str(prod_dct.get('itemId')),
                        'title': title,
                        'description': description,
                        # здесь отсутствует url товара (карточки товара)
                        'url': '',
                        'url_picture': prod_dct.get('mainImg'),
                        'time_scrap': str(datetime.datetime.now().isoformat()),
                        'sub_category': cat_tpl[1],
                        'category_full_path': f'{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}',
                        'brand': '',
                        'cost': str(int(prod_dct.get('price')/100)),
                        'prev_cost': str(prev_price),
                        'measure': measure,
                        'city': self.city,
                            }

                        self.rezult.append(l) 
                else:
                    # Кочились страницы категории. Добавим категорию в список для обновления scrap_count
                    d = {
                        'id': cat_tpl[0],
                        'key_column': self.city + '/' + cat_tpl[0],
                        'scrap_count': cat_tpl[4] + 1 
                    }
                    self.category_update.append(d)

                    break
                
                print(f'Magnum {self.city} - страница {page + 1} категории "{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}" запрос {req_cnt}')
                rand_pause()

    def __upload_to_db(self):
        
        # грузим "спарсенные" данные в базу
        print(f'Magnum - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')
        
        # обновляем scrap_count для "спарсеных" категорий 3-го уровня
        update_category_mgm_air(self.category_update, DB_PATH, DB_MGM_CATEGORY_TABLE, 'key_column')

        # после того как обновили scrap_count для "спарсеных" категорий 3-го уровня,
        # обновим scrap_count для родительской категории (2-го уровня) - возьмем наименьшее scrap_count среди дочерних категорий
        parent_set = {i[6] for i in self.category_list}
        for par_id in parent_set:
            filter_ls = [('parent_id', par_id), ('city', self.city)]
            update_parent_category_mgm(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE, pk_column='key_column', filter_ls=filter_ls)

        # после того как обновили scrap_count для категорий 2-го уровня,
        # обновим scrap_count для родительской категории (1-го уровня) - возьмем наименьшее scrap_count среди дочерних категорий
        parent_set = {i[7] for i in self.category_list}
        for par_id in parent_set:
            filter_ls = [('parent_id', par_id), ('city', self.city)]
            update_parent_category_mgm(db_path=DB_PATH, table_name=DB_MGM_CATEGORY_TABLE, pk_column='key_column', filter_ls=filter_ls)



    def start(self):
        self.fill_category_table()
        self.fill_category_data()
        self.__upload_to_db()


def fast_category_scraper(city):

    # Овощи, фрукты, ягоды, зелень, грибы
    fast_category = '1103'
    print(f'Run for city - {city}')
    magnum = MagnumScrapper(city=city, fast_category_id=fast_category)
    magnum.start()


def main():
    # city = (sys.argv[1] if len(sys.argv) > 1 else 'almaty')
    city = (sys.argv[1] if len(sys.argv) > 1 else 'astana')
    print(f'Run for city - {city}')
    magnum = MagnumScrapper(city=city)
    magnum.start()


if __name__ == '__main__':
    main()
