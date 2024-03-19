from scr.volt_fetchs import PARAMS_TOKEN, URL_TOKEN, REFRESH_TOKEN_MASK, \
                                URL_CATEGORY, PARAMS_CATEGORY,CURRENT_CATEGORY_MASK, URL_CATALOG, PARAMS_CATALOG
import datetime
from scr.share_functions import get_fetch, format_name
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_vlt, \
                                get_data_from, truncate_table, create_table
from constants.constants import DB_PATH, DB_VLT_CATEGORY_TABLE, DB_VLT_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE, DB_VLT_REFRESH_TOKEN_TABLE, DB_VLT_REFRESH_TOKEN_CREATE_STR
import random



class VoltScrapper():
    def __init__(self, fast_category_ls=None) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.fast_category_ls = fast_category_ls
        self.refresh_token = None
        self.userlocationlng = f'76.{str(random.randint(889433, 960513))}'
        self.userlocationlat = f'43.2{str(random.randint(32015, 49646))}'
        self.token = None
        self.create_refresh_token_table()
        # self.get_token()
        


    def create_refresh_token_table(self):
        create_table(db_path=DB_PATH, 
                     table_name=DB_VLT_REFRESH_TOKEN_TABLE,
                     table_create_str=DB_VLT_REFRESH_TOKEN_CREATE_STR)


    def get_token(self):

        if not self.refresh_token:
            result = get_data_from(
                        db_path=DB_PATH,
                        table_name=DB_VLT_REFRESH_TOKEN_TABLE,
                        columns='refresh_token',
                        filter_tpl=tuple())
            
            if isinstance(result, list) and result:
                self.refresh_token = result[0][0]
    
        if self.refresh_token:
            if not self.token:
                PARAMS_TOKEN['body'] = PARAMS_TOKEN['body'].replace(REFRESH_TOKEN_MASK, self.refresh_token)

                resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
                resp_js = resp.json()
                
                if resp_js['access_token']:
                    self.token = resp_js['access_token']
                    
                    done = truncate_table(db_path=DB_PATH, 
                                table_name=DB_VLT_REFRESH_TOKEN_TABLE)
                    
                    if done:
                        upload_to_db(rezult=[{'refresh_token': resp_js['refresh_token']}], 
                                    db_path=DB_PATH, 
                                    table_name=DB_VLT_REFRESH_TOKEN_TABLE,
                                    table_create_str=DB_VLT_REFRESH_TOKEN_CREATE_STR,
                                    pk_column='refresh_token')


    def fill_category_table(self):
        '''Создает и перезаполняет актуальными данными таблицу категорий, если она не существует'''

        if not self.token:
            self.get_token()

        if self.token:
            if not table_exists(db_path=DB_PATH, table_name=DB_VLT_CATEGORY_TABLE):

                # для самого верхнего уровня категорий PARENT_ID пустой
                params_head = PARAMS_CATEGORY.copy()
                params_head['headers']['Authorization'] = f'Bearer {self.token}'
                params_head['headers']['userlocationlng'] = self.userlocationlng
                params_head['headers']['userlocationlat'] = self.userlocationlat
                
                resp = get_fetch(url=URL_CATEGORY, params=params_head)
                resp_js = resp.json()
                cetegoly_ls = resp_js.get('categories')

                if cetegoly_ls:
                    for head_dct in cetegoly_ls:
                        
                        if not head_dct.get('parent_category_id'):
                            name = format_name(head_dct.get('name'))

                            # добавляем категорию 
                            dct = {
                                'id': str(head_dct.get('id')),
                                'name': str(name.strip()),
                                }

                            print(f"Получаем категорию id={head_dct['id']}, {name}")

                            self.category_list.append(dct)

                    if self.category_list:
                        upload_to_db(rezult=self.category_list, 
                                    db_path=DB_PATH, 
                                    table_name=DB_VLT_CATEGORY_TABLE,
                                    table_create_str=DB_VLT_CATEGORY_CREATE_STR,
                                    pk_column='id')
            
        else:
            print('Токен отсутствует')


    def fill_category_data(self):
        '''Парсит данные по нужным категориям'''

        if self.token:

            self.category_list = get_next_categoy_vlt(db_path=DB_PATH, 
                                                    table_name=DB_VLT_CATEGORY_TABLE, 
                                                    pk_column='id',
                                                    fast_category_ls = self.fast_category_ls)
            
            # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
            req_cnt = 0
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

                        for cat in categories:
                            if cat['id'] == prod_dct.get('category'):
                                sub_category_name = format_name(cat['name'])
                                parent_category_id = cat['parent_category_id']

                                for parent_cat in categories:
                                    if parent_cat['id'] == parent_category_id:
                                        category_name = format_name(parent_cat['name'])
                        
                        unformatted_unit_price = prod_dct.get('unformatted_unit_price')
                        if unformatted_unit_price:
                            cost = str(int(unformatted_unit_price.get('price')/100))

                            if unformatted_unit_price.get('original_price'): 
                                prev_cost = str(int(unformatted_unit_price.get('original_price')/100))
                            else:
                                prev_cost = '0'

                        else:
                            cost = str(int(prod_dct.get('baseprice')/100)) 
                            prev_cost = '0'
                        
                        l = {
                        'mercant_id': MERCANTS['vlt'],
                        'mercant_name': 'vlt',
                        'product_id': str(prod_dct.get('id')),
                        'title': title,
                        'description': description,
                        # здесь отсутствует url товара (карточки товара)
                        'url': '',
                        'url_picture': prod_dct.get('image'),
                        'time_scrap': str(datetime.datetime.now().isoformat()),
                        'sub_category': sub_category_name,
                        'category_full_path': f'/{category_name}/{sub_category_name}',
                        'brand': '',
                        'cost': cost,
                        'prev_cost': prev_cost
                            }

                        sku_count += 1
                        self.rezult.append(l) 

                    
                print(f'Volt -  категория "/{category_name}/" товаров {sku_count}')

        else:
            print('Токен отсутствует')

    def __upload_to_db(self):
        
        # грузим "спарсенные" данные в базу
        print(f'Volt - получено {len(self.rezult)} sku')
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')


    def start(self):
        self.fill_category_table()
        self.fill_category_data()
        self.__upload_to_db()


def fast_category_scraper():

    # Овощи, фрукты, ягоды, зелень, грибы
    fast_category_ls = [
        '63443f7efed9bfd239e95b31',
        '64ca2414e3523f7a1e86fbd6'
    ]

    volt = VoltScrapper(fast_category_ls=fast_category_ls)
    volt.start()


def main():
    volt = VoltScrapper()
    volt.start()

def initiate():
    volt = VoltScrapper()
    volt.create_refresh_token_table()


if __name__ == '__main__':
    main()
