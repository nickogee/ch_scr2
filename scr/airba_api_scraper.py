from scr.airba_fetch import PAGE, CATALOG, WORKFLOW, URL_CATEGORY, PARAMS_CATEGORY, \
                                REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
import datetime
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm_air, \
                                update_category_mgm_air, update_parent_category_mgm_air
from constants.constants import DB_PATH, DB_AIR_CATEGORY_TABLE, DB_AIR_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, CITY_POSTFIX


class AirbaScrapper():
    def __init__(self, fast_category_id=None) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.fast_category_id = fast_category_id
        self.limit_off = bool(fast_category_id)
        self.workflow = WORKFLOW
        self.city = 'almaty'
    
    def fill_category_table(self):
        '''Создает и перезаполняет актуальными данными таблицу категорий, если она не существует'''

        if not table_exists(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE):

            # для самого верхнего уровня категорий PARENT_ID пустой
            params_head = PARAMS_CATEGORY.copy()
            params_head['headers']['workflow'] = self.workflow
            
            resp = get_fetch(url=URL_CATEGORY, params=params_head)
            resp_js = resp.json()
            data = resp_js['data']

            for head_dct in data:
                # категория с  id = 0 - это категория "Все"
                if head_dct['id'] == 0:
                    continue
                
                # добавляем категорию первого уровня
                head_id = str(head_dct['id'])
                dct = {
                    'parent_id': '',
                    'id': head_id,
                    'name': str(head_dct['section']),
                    'category_lvl': '1',
                }

                print(f"- Получаем категорию id={head_dct['id']}, name={head_dct['section']}")
                self.category_list.append(dct)

                chld_ls = head_dct.get('categories')
                if chld_ls:
                    for chld_dct in chld_ls:
                        
                        # добавляем категорию второго уровня
                        chld_id = str(chld_dct['id'])
                        dct = {
                        'parent_id': head_id,
                        'id': chld_id,
                        'name': str(chld_dct['name']),
                        'category_lvl': '2',
                                }
                        
                        print(f"-- Получаем категорию id={chld_dct['id']}, name={chld_dct['name']}")
                        self.category_list.append(dct)

                        sub_chld_ls = chld_dct['items']
                        for sub_chld_dct in sub_chld_ls:

                            # добавляем категорию третьего уровня
                            sub_chld_id = str(sub_chld_dct['id'])
                            dct = {
                            'parent_id': chld_id,
                            'id': sub_chld_id,
                            'name': str(sub_chld_dct['name']),
                            'category_lvl': '3',
                                }

                            print(f"--- Получаем категорию id={sub_chld_dct['id']}, name={sub_chld_dct['name']}")
                            self.category_list.append(dct)

                            rand_pause(10)

                            # для каждой категории третьего уровня делаем запрос, чтобы получить дочерние категории (4-го уровня)
                            params_chld = PARAMS_CATEGORY.copy()
                            params_chld['headers']['workflow'] = self.workflow
                            
                            chld_resp = get_fetch(url=f'{URL_CATEGORY}{sub_chld_id}/', params=params_chld)
                            chld_resp_js = chld_resp.json()
                            chld_data = chld_resp_js['data']

                            for i in chld_data:

                                # добавляем категорию четвертого уровня
                                i_id = str(i['id'])
                                dct = {
                                'parent_id': sub_chld_id,
                                'id': i_id,
                                'name': str(i['name']),
                                'category_lvl': '4',
                                    }

                                print(f"---- Получаем категорию id={i['id']}, name={i['name']}")
                                self.category_list.append(dct)
                

            if self.category_list:
                upload_to_db(rezult=self.category_list, 
                            db_path=DB_PATH, 
                            table_name=DB_AIR_CATEGORY_TABLE,
                            table_create_str=DB_AIR_CATEGORY_CREATE_STR,
                            pk_column='id')

    def fill_category_data(self):
        '''Парсит данные по нужным категориям'''
        
        self.category_list = get_next_categoy_list_mgm_air(db_path=DB_PATH, 
                            table_name=DB_AIR_CATEGORY_TABLE, mercant='air', cat_lvl='3', fast_category_id=self.fast_category_id)
        
        # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
        req_cnt = 0
        for cat_tpl in self.category_list:

            if (not self.limit_off) and (req_cnt > REQ_LIMIT):
                break
            
            # текущая категория 4-го уровня
            catalog_di = cat_tpl[0]

            # условие выхода из цикла: текущая страница - последняя
            is_last_page = False

            # текущая страница
            page = 1

            while not is_last_page:

                params = PARAMS_CATALOG.copy()
                
                param_path = params['headers']['path']
                param_path = param_path.replace(PAGE, str(page))
                param_path = param_path.replace(CATALOG, str(catalog_di))
                
                params['headers']['path'] = param_path
                params['headers']['workflow'] = self.workflow

                params['params']['category'] = str(catalog_di)
                params['params']['page'] = str(page)
                
                resp = get_fetch(url=URL_CATALOG, params=params)
                
                req_cnt += 1
                page += 1

                if resp.status_code == 200:
                    resp_js = resp.json()
                    data = resp_js.get('data')

                    if data:

                        products = data.get('products')

                        if products: 
                        
                            #  проверяем, последняя ли это страница
                            products_page = products.get('page')
                            products_total_page = products.get('total_pages')
                            is_last_page = (products_page == products_total_page)

                            results_ls = products.get('results')
                            if results_ls:

                                for prod_dct in results_ls:

                                    title = prod_dct.get('name')
                                    title = title.replace('«', '')
                                    title = title.replace('»', '')
                                    title = title.replace('"', '')
                                    title = title.replace("'", '')
                                
                                    description = prod_dct.get('description')
                                    if description:
                                        description = description.replace('«', '')
                                        description = description.replace('»', '')
                                        description = description.replace('"', '')
                                        description = description.replace("'", '')
                                    else:
                                        description = ''

                                    images_ls = prod_dct.get('images')
                                    if images_ls:
                                        image = images_ls[0]['image_origin_url']
                                    else:
                                        image = ''

                                    category_dct = prod_dct.get('category')
                                    if category_dct:
                                        category_full_path = category_dct.get('full_hierarchy')
                                    else:
                                        category_full_path = f'{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}'


                                    prev_cost = prod_dct.get('price_previous')
                                    if isinstance(prev_cost, (int, float)):
                                        prev_cost = int(prev_cost)
                                    else:
                                        prev_cost = 0
                                    

                                    brand = str(prod_dct.get('brand'))
                                    if brand:
                                        brand = brand.replace('«', '')
                                        brand = brand.replace('»', '')
                                        brand = brand.replace('"', '')
                                        brand = brand.replace("'", '')
                                    else:
                                        brand = ''

                                    mercant_short_name = 'air' + '-' + CITY_POSTFIX[self.city]

                                    l = {
                                    'mercant_id': MERCANTS[mercant_short_name],
                                    'mercant_name': mercant_short_name,
                                    'product_id': str(self.city + '_' + str(prod_dct.get('id'))),
                                    'id': str(prod_dct.get('id')),
                                    'title': title,
                                    'description': description,
                                    'url': '', # здесь отсутствует url товара (карточки товара)
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

                                    self.rezult.append(l) 

                else:
                    is_last_page = True

                print(f'Fresh Airba - страница {page - 1} категории "{cat_tpl[3]}/{cat_tpl[2]}/{cat_tpl[1]}" запрос {req_cnt}')
                rand_pause()

            else:
                 # Кочились страницы категории. Добавим категорию в список для обновления scrap_count
                d = {
                    'id': cat_tpl[0],
                    'scrap_count': cat_tpl[4] + 1 
                    }
                self.category_update.append(d)

    def __upload_to_db(self):
        
        # грузим "спарсенные" данные в базу
        print(f'Fresh Airba - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')
        
        # обновляем scrap_count для "спарсеных" категорий 4-го уровня
        update_category_mgm_air(self.category_update, DB_PATH, DB_AIR_CATEGORY_TABLE, 'id')

        # после того как обновили scrap_count для "спарсеных" категорий 4-го уровня,
        # обновим scrap_count для родительской категории (3-го уровня) - возьмем наименьшее scrap_count среди дочерних категорий
        parent_set = {i[6] for i in self.category_list}
        for par_id in parent_set:
            # filter_tpl = ('parent_id', self.category_list[0][6])
            filter_tpl = ('parent_id', par_id)
            update_parent_category_mgm_air(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl)

        # после того как обновили scrap_count для категорий 3-го уровня,
        # обновим scrap_count для родительской категории (2-го уровня) - возьмем наименьшее scrap_count среди дочерних категорий
        parent_set = {i[7] for i in self.category_list}
        for par_id in parent_set:
            # filter_tpl = ('parent_id', self.category_list[0][7])
            filter_tpl = ('parent_id', par_id)
            update_parent_category_mgm_air(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl)

        # после того как обновили scrap_count для категорий 2-го уровня,
        # обновим scrap_count для родительской категории (1-го уровня) - возьмем наименьшее scrap_count среди дочерних категорий
        parent_set = {i[7] for i in self.category_list}
        for par_id in parent_set:
            # filter_tpl = ('parent_id', self.category_list[0][8])
            filter_tpl = ('parent_id', par_id)
            update_parent_category_mgm_air(db_path=DB_PATH, table_name=DB_AIR_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl)

        

    def start(self):
        self.fill_category_table()
        self.fill_category_data()
        self.__upload_to_db()


def fast_category_scraper():

    fast_category_ls = [
        '1782', # Фрукты, ягоды
        '1785'  # Овощи, грибы и зелень
    ]

    for fast_category in fast_category_ls:
        airba = AirbaScrapper(fast_category)
        airba.start()    


def main():
    airba = AirbaScrapper()
    airba.start()


if __name__ == '__main__':
    main()


