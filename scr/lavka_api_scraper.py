from scr.lavka_fetchs import PARAMS_TOKEN, URL_TOKEN, LAT_MASK, LONG_MASK, CURRENT_CATEGORY_ID_MASK, CURRENT_CATEGORY_MASK,\
                                LAYOUT_ID_MASK, PARAMS_CATALOG, URL_CATALOG
                                # URL_CATEGORY, PARAMS_CATEGORY, CURRENT_CATEGORY_MASK, URL_CATALOG, PARAMS_CATALOG
import datetime
from scr.share_functions import get_fetch, format_name, get_new_session
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
        self.userlocationlng = 76.881999
        self.userlocationlat = 43.217141
        self.geoId = 'eaeda5a3eb5daf7bf92baab01d86baed029b7aed8546291e3d892c3dcc0fe05c'
        self.layout_id = '40bcdf6504ef04e6c4c876adb789444d'
        self.token = None
        self.skillet_html = None
        self.session = None
        self.city = 'almaty'


    def prepare_for_connect(self):
        self._get_skillet_html()
        self.get_token()
        self.get_layout_id()
        self.get_geodata()

    def _get_skillet_html(self):
        session = get_new_session()
        session.headers = PARAMS_TOKEN['headers']
        self.session = session
        resp = session.get(url=URL_TOKEN, params=PARAMS_TOKEN)

        # resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
        self.skillet_html = resp.text
        
        # with open('/Users/hachimantaro/Desktop/lavka_skilet.html', 'r', encoding='utf-8') as hlml_file:
        #     self.skillet_html = hlml_file.read()


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
        pattern_geoId = re.compile("\"buildingId\":\s?\"[a-zA-Z0-9]*\"")

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

    def saturate_cookie(self):

        url_2bdb182 = 'https://lavka.yandex.kz/api/i18n/2bdb1827adf72fb60ef24e6205c52c98-ru'

        headers_2bdb182 = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'connection':'keep-alive',
            'host': 'api.passport.yandex.kz',
            'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        resp_2bdb182 = self.session.get(url=url_2bdb182, headers=headers_2bdb182)
        print(resp_2bdb182.text)

        url_tag = 'https://mc.yandex.ru/metrika/tag.js'

        headers_tag = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'referer': 'https://lavka.yandex.kz/',
            'priority': 'u=4, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        resp_tag = self.session.get(url=url_tag, headers=headers_tag)
        print(resp_tag.text)

        url_click = 'https://yandex.ru/clck/click'

        headers_click = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'connection':'keep-alive',
            'content-length':'827',
            'content-type':'text/plain;charset=UTF-8',
            'host': 'api.passport.yandex.kz',
            'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'priority': 'u=4, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        body_click = r'/reqid=0b9bf222-e68e-4332-ac57-27010dfbe5fe/path=690.2096.207/vars=-env=production,-page=%2F,-platform=desktop,-project=lavkaweb,-version=292.2.0,-additional=%7B%22cType%22%3A%22stable%22%2C%22nodeId%22%3A%22node-2%22%2C%22taxiUserId%22%3A%22ab170d1b7a2b4a5f8814d37218b48917%22%2C%22traceId%22%3A%2271b88b67-664c-4067-af4b-3a5562aa20b4%22%2C%22realRequestId%22%3A%2275d93024-e8be-43eb-955f-4d349468410e%22%2C%22passportStatus%22%3A%22INVALID_PARAMS%22%2C%22passportError%22%3A%22BlackBox%20error%3A%20Missing%20sessionid%20argument.%22%2C%22language%22%3A%22ru%22%2C%22application%22%3A%22yandex%22%2C%22rtl%22%3Afalse%7D,rum_id=ru.lavkaweb.desktop,experiments=snippet_redesign.enabled%3Dfalse%3Bresponsiveness-config.simpleHtmlParser%3Dfalse,region=162,143.2129=1736941263682,1701=2876,207=1173.9,-cdn=mskm/cts=1736941264856/*'
        resp_click = self.session.post(url=url_click, headers=headers_click, data=body_click)
        print(resp_click.text)


        url_advert = 'https://mc.yandex.ru/metrika/advert.gif'
        headers_advert = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'priority': 'i',
            # 'connection':'keep-alive',
            # 'host': 'api.passport.yandex.kz',
            # 'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        resp_advert = self.session.get(url=url_advert, headers=headers_advert)

        print(resp_advert.text)


        url_mc_yandex = 'https://mc.yandex.ru/watch/3?wmode=7&page-url=https%3A%2F%2Flavka.yandex.kz%2F&page-ref=&charset=utf-8&ut=noindex&browser-info=pv%3A1%3Avf%3A14pwap7gbnncs44tf8xglmzmddy7%3Afu%3A0%3Aen%3Autf-8%3Ala%3Aru-RU%3Av%3A1560%3Acn%3A1%3Adp%3A0%3Als%3A521690245262%3Ahid%3A542792463%3Az%3A300%3Ai%3A20250115164105%3Aet%3A1736941265%3Ac%3A1%3Arn%3A200000786%3Arqn%3A3%3Au%3A1736941265955622872%3Aw%3A295x838%3As%3A1512x982x30%3Ask%3A2%3Awv%3A2%3Aco%3A0%3Acpf%3A1%3Ans%3A1736941263682%3Ast%3A1736941265&t=mc(p-2)clc(0-0-0)rqnt(3)aw(1)rcm(1)yu(7618510031736941264)ecs(0)cdl(na)eco(65536)ti(1)'
        headers_mc_yandex = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            # 'connection':'keep-alive',
            # 'host': 'api.passport.yandex.kz',
            'origin': 'https://lavka.yandex.kz',
            'priority': 'u=1, i',
            'referer': 'https://lavka.yandex.kz/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cors-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        resp_mc_yandex = self.session.get(url=url_mc_yandex, headers=headers_mc_yandex)

        print(resp_mc_yandex.text)


        url_state = 'https://lavka.yandex.kz/api/v1/providers/v1/state'

        headers_state = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'connection':'keep-alive',
            'content-length':'47',
            'content-type':'application/json',
            'host': 'lavka.yandex.kz',
            'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'priority': 'u=4, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-captcha-language': 'ru',
            'x-captcha-service': 'lavka',
            'x-csrf-token': self.token,
            'x-lavka-web-city': '162',
            'x-lavka-web-locale': 'ru-KZ',
            'x-requested-with': 'XMLHttpRequest',
        }

        body_state = r'{"position":{"location":[76.881999,43.217141]}}'
        resp_state = self.session.post(url=url_state, headers=headers_state, data=body_state)
        print(resp_state.text)


        url_check = 'https://api.passport.yandex.kz/registration_status/check?origin=grocery-frontend-standalone'
        headers_check = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'connection':'keep-alive',
            'host': 'api.passport.yandex.kz',
            'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',

        }
        resp_check = self.session.get(url=url_check, headers=headers_check)

        print(resp_check.text)


        url_get_data = 'https://lavka.yandex.kz/api/v1/app/v1/get-data'
        headers_get_data = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language':'ru-RU,ru;q=0.9',
            'connection':'keep-alive',
            'host': 'lavka.yandex.kz',
            # 'origin': 'https://lavka.yandex.kz',
            'referer': 'https://lavka.yandex.kz/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "macOS",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-captcha-language': 'ru',
            'x-captcha-service': 'lavka',
            'x-csrf-token': self.token,
            'x-lavka-web-city': '162',
            'x-lavka-web-locale': 'ru-KZ',
            'x-requested-with': 'XMLHttpRequest',
        }
        resp_get_data = self.session.get(url=url_get_data, headers=headers_get_data)

        print(resp_get_data.text)

















    def fill_category_data(self):
        '''Парсит данные по нужным категориям'''

        if self.token:

    #         self.category_list = get_next_categoy_vlt(db_path=DB_PATH, 
    #                                                 table_name=DB_VLT_CATEGORY_TABLE, 
    #                                                 pk_column='id',
    #                                                 fast_category_ls = self.fast_category_ls)
            
            self.category_list = [('95de73852b72b4dec7be9d74bfe4c781', 'milk_butter_eggs')]
            
            PARAMS_CATALOG['headers']['Referer'] = PARAMS_CATALOG['headers']['Referer'].replace(CURRENT_CATEGORY_MASK, self.category_list[0][1])
            PARAMS_CATALOG['headers']['X-Csrf-Token'] = self.token
            PARAMS_CATALOG['body'] = PARAMS_CATALOG['body'].replace(CURRENT_CATEGORY_MASK, self.category_list[0][1])
            PARAMS_CATALOG['body'] = PARAMS_CATALOG['body'].replace(CURRENT_CATEGORY_ID_MASK, self.category_list[0][0])
            PARAMS_CATALOG['body'] = PARAMS_CATALOG['body'].replace(LAYOUT_ID_MASK, self.layout_id)
            PARAMS_CATALOG['body'] = PARAMS_CATALOG['body'].replace(LAT_MASK, self.userlocationlat)
            PARAMS_CATALOG['body'] = PARAMS_CATALOG['body'].replace(LONG_MASK, self.userlocationlng)
            PARAMS_CATALOG['headers']['Content-Length'] = len(PARAMS_CATALOG['body']) +1
            
            resp = self.session.post(url=URL_CATALOG, params=PARAMS_CATALOG, data=PARAMS_CATALOG['body'])
            print(resp.text)
            
            
            
            
            
            # будет содержать текущее количество выполненных запросов, чтобы не привысить лимит запростов
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
        self.prepare_for_connect()
        self.fill_category_table()
        self.saturate_cookie()
        self.fill_category_data()
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
