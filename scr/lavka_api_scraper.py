from scr.lavka_fetchs import PARAMS_TOKEN, URL_TOKEN
                                # URL_CATEGORY, PARAMS_CATEGORY, CURRENT_CATEGORY_MASK, URL_CATALOG, PARAMS_CATALOG
import datetime
from scr.share_functions import get_fetch, format_name
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_vlt, \
                                get_data_from, truncate_table, create_table
from constants.constants import DB_PATH, DB_LVK_CATEGORY_TABLE, DB_LVK_CATEGORY_CREATE_STR, MERCANTS, CITY_POSTFIX,\
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE
import json
import re
from bs4 import BeautifulSoup

class VoltScrapper():
    def __init__(self, fast_category_ls=None) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.fast_category_ls = fast_category_ls
        self.userlocationlng = 0
        self.userlocationlat = 0
        self.geoId = None
        self.layout_id = None
        self.token = None
        self.skillet_html = None
        self.city = 'almaty'


    def prepare_saens_data(self):
        self._get_skillet_html()
        self.get_token()
        self.get_layout_id()
        self.get_geodata()

    def _get_skillet_html(self):
        resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
        self.skillet_html = resp.text
        
        with open('/Users/hachimantaro/Desktop/lavka_skilet.html', 'r', encoding='utf-8') as hlml_file:
            self.skillet_html = hlml_file.read()


    def get_token(self):
        pattern = re.compile("\"csrfToken\":\s?\"[a-z0-9]*:[0-9]{10}\"")

        # sj_script = soup.find(name='script', string=pattern)
        # if sj_script:
        token_ls = re.findall(pattern, self.skillet_html)
        if token_ls:
            token_row = token_ls[0].replace('"csrfToken":', '')
            self.token = token_row.replace('"', '')
            print (f"token - {self.token}")
        else:
            print('Не найдено значение token')


    def get_layout_id(self):
        pattern = re.compile("\"layoutId\":\s?\"[a-z0-9]*\"")
        layout_id_ls = re.findall(pattern, self.skillet_html)
        if layout_id_ls:
            layout_id_row = layout_id_ls[0].replace('"layoutId":', '')
            self.layout_id = layout_id_row.replace('"', '')
            print (f"layout_id - {self.layout_id}")
        else:
            print('Не найдено значение layout_id')


    def get_geodata(self):
        pattern_long = re.compile("\"lon\":\s?[0-9]{2}.[0-9]{6}")
        pattern_lat = re.compile("\"lat\":\s?[0-9]{2}.[0-9]{6}")
        pattern_geoId = re.compile("\"buildingId\":\s?\"[a-z0-9]*\"")

        long_ls = re.findall(pattern_long, self.skillet_html)
        lat_ls = re.findall(pattern_lat, self.skillet_html)
        geoId_ls = re.findall(pattern_geoId, self.skillet_html)

        if long_ls:
            long_row = long_ls[0].replace('"lon":', '')
            self.userlocationlng = long_row.replace('"', '')
            print (f"userlocationlng - {self.userlocationlng}")
        else:
            print('Не найдено значение userlocationlng')
        
        if lat_ls:
            row = lat_ls[0].replace('"lat":', '')
            self.userlocationlat = row.replace('"', '')
            print (f"userlocationlat - {self.userlocationlat}")
        else:
            print('Не найдено значение userlocationlat')
        
        if geoId_ls:
            row = geoId_ls[0].replace('"buildingId":', '')
            self.geoId = row.replace('"', '')
            print (f"geoId - {self.geoId}")
        else:
            print('Не найдено значение geoId')
        



    def fill_category_table(self):
        '''Создает и перезаполняет актуальными данными таблицу категорий, если она не существует'''

        if not table_exists(db_path=DB_PATH, table_name=DB_LVK_CATEGORY_TABLE):
            if not self.skillet_html:
                self._get_skillet_html()

            if self.skillet_html:
                soup = BeautifulSoup(self.skillet_html , 'html.parser')
                catalog = soup.find(name='nav', attrs={'aria-label': "Каталог"})
                
                li_list = catalog.find_all('li')
                for li in li_list:
                    category_name = None

                    button = li.find(name='button')
                    if button:

                        # ищем id категории
                        div_list = li.find_all(name='div', recursive=False)
                        if div_list and div_list[0].has_attr('data-item-id'):
                            category_id = div_list[0]['data-item-id']

                        # ищем имя категории
                        span_list = button.find_all(name='span')
                        for span in span_list:
                            if not span.has_attr('style'):
                                category_name = span.text

                        sub_li_list = li.find_all(name='li')
                        for sub_li in sub_li_list:
                            if sub_li.has_attr('data-item-id'):
                                # ищем id подкатегории
                                sub_categoty_id = sub_li['data-item-id']

                                # ищем диплинк
                                a = sub_li.find(name='a')
                                if a and a.has_attr('href'):
                                    sub_categoty_href = a['href']
                                
                                # ищем имя подкатегории
                                if a:
                                    a_span = a.find(name='span')
                                    if a_span:
                                        sub_categoty_name = a_span.text
                                
                                # добавляем запись подкатегории 
                                dct = {
                                    'sub_category_id': sub_categoty_id,
                                    'category_id': category_id,
                                    'sub_category_name': sub_categoty_name,
                                    'category_name': category_name,
                                    'sub_categoty_href': sub_categoty_href,
                                    'city': self.city,
                                    'key_column': f'{self.city}/{sub_categoty_id}',
                                    }
                                
                                print(f'Получаем категорию - {category_name}/{sub_categoty_name}', 
                                    f'categoty_id - {category_id}',
                                    f'sub_categoty_id - {sub_categoty_id}',
                                    f'href - {sub_categoty_href}', sep='|')

                                self.category_list.append(dct)

                if self.category_list:
                    upload_to_db(rezult=self.category_list, 
                                db_path=DB_PATH, 
                                table_name=DB_LVK_CATEGORY_TABLE,
                                table_create_str=DB_LVK_CATEGORY_CREATE_STR,
                                pk_column='key_column')
                else:
                    print('Не удалось получить список категорий для создания таблицы категорий')


    # def fill_category_data(self):
    #     '''Парсит данные по нужным категориям'''

    #     if self.token:

    #         self.category_list = get_next_categoy_vlt(db_path=DB_PATH, 
    #                                                 table_name=DB_VLT_CATEGORY_TABLE, 
    #                                                 pk_column='id',
    #                                                 fast_category_ls = self.fast_category_ls)
            
    #         # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
    #         req_cnt = 0
    #         for cat_dct in self.category_list:

    #             params = PARAMS_CATALOG.copy()
    #             params['headers']['path'] = params['headers']['path'].replace(CURRENT_CATEGORY_MASK, cat_dct['id'])
    #             params['headers']['Authorization'] = f'Bearer {self.token}'
    #             params['headers']['userlocationlng'] = self.userlocationlng
    #             params['headers']['userlocationlat'] = self.userlocationlat

    #             url = URL_CATALOG.replace(CURRENT_CATEGORY_MASK, cat_dct['id'])
    #             resp = get_fetch(url=url, params=params)
    #             resp_js = resp.json()

    #             categories = resp_js.get('categories')

    #             content = resp_js.get('items')
    #             if content:
                    
    #                 sku_count = 0
    #                 for prod_dct in content:
    #                     title = prod_dct.get('name')
    #                     title = title.replace('«', '')
    #                     title = title.replace('»', '')
    #                     title = title.replace('"', '')
    #                     title = title.replace("'", '')
                            
    #                     description = prod_dct.get('description')
    #                     if description:
    #                         description = description.replace('«', '')
    #                         description = description.replace('»', '')
    #                         description = description.replace('"', '')
    #                         description = description.replace("'", '')
    #                     else:
    #                         description = ''

    #                     category_name = None
    #                     sub_category_name = None
                        
    #                     for cat in categories:
    #                         if cat['id'] == prod_dct.get('category'):
    #                             sub_category_name = format_name(cat['name'])
    #                             parent_category_id = cat['parent_category_id']

    #                             for parent_cat in categories:
    #                                 if parent_cat['id'] == parent_category_id:
    #                                     category_name = format_name(parent_cat['name'])
                        
    #                     if not sub_category_name:
    #                         sub_category_name = '<empty>'
    #                         print(f'Не найдена подкатегория для {title}')
                        
    #                     if not category_name:
    #                         category_name = '<empty>'
    #                         print(f'Не найдена родительская категория для {title}')

    #                     unformatted_unit_price = prod_dct.get('unformatted_unit_price')
    #                     if unformatted_unit_price:
    #                         cost = str(int(unformatted_unit_price.get('price')/100))

    #                         if unformatted_unit_price.get('original_price'): 
    #                             prev_cost = str(int(unformatted_unit_price.get('original_price')/100))
    #                         else:
    #                             prev_cost = '0'

    #                     else:
    #                         cost = str(int(prod_dct.get('baseprice')/100)) 
    #                         prev_cost = '0'
                        
    #                     mercant_short_name = 'vlt' + '-' + CITY_POSTFIX[self.city]

    #                     l = {
    #                     'mercant_id': MERCANTS[mercant_short_name],
    #                     'mercant_name': mercant_short_name,
    #                     'product_id': str(self.city + '_' + str(prod_dct.get('id'))),
    #                     'id': str(prod_dct.get('id')),
    #                     'title': title,
    #                     'description': description,
    #                     # здесь отсутствует url товара (карточки товара)
    #                     'url': '',
    #                     'url_picture': prod_dct.get('image'),
    #                     'time_scrap': str(datetime.datetime.now().isoformat()),
    #                     'sub_category': sub_category_name,
    #                     'category_full_path': f'/{category_name}/{sub_category_name}',
    #                     'brand': '',
    #                     'cost': cost,
    #                     'prev_cost': prev_cost,
    #                     'measure': prod_dct.get('unit_info'),
    #                     'city': self.city,
    #                         }

    #                     sku_count += 1
    #                     self.rezult.append(l) 

                    
    #                 print(f'Volt {self.city} -  категория "/{category_name}/" товаров {sku_count}')

    #     else:
    #         print('Токен отсутствует')

    # def __upload_to_db(self):
        
    #     # грузим "спарсенные" данные в базу
    #     print(f'Volt {self.city} - получено {len(self.rezult)} sku')
    #     upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'product_id')


    def start(self):
        self.prepare_saens_data()
        self.fill_category_table()
        # self.fill_category_data()
        # self.__upload_to_db()


# def fast_category_scraper():

#     fast_category_ls = [
#             '73400dc454444536b021ee99',
#             'fa11fe7023bb4bd8822ec45d',
#         ]

#     volt = VoltScrapper(fast_category_ls=fast_category_ls)
#     volt.start()


def main():
    volt = VoltScrapper()
    volt.start()



if __name__ == '__main__':
    main()
