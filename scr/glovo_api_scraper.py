from scr.glovo_fetchs import PARAMS, URL_SERV, URL_FST, SLUG
import datetime
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, get_next_categoy_glv
from constants import DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, MERCANTS,\
                                        DB_GLV_CATEGORY_TABLE, DB_GLV_CATEGORY_CREATE_STR
                                    


class GlovoApiScraper():

    def __init__(self, cat_dct):
        self.categorie_dict = cat_dct
        self.rezult = []
        self.head_response = get_fetch(URL_FST.replace(SLUG, cat_dct['slug']), PARAMS)
        self.categories = self.head_response.json()['data']['body'][0]['data']['elements']
        self.df = None
        self.date_time_now = datetime.datetime.now()

    def fill_rezult(self):

        for curr_category in self.categories:
            category_name = curr_category['data']['title']
            cat_route = curr_category['data']['action']['data']['path']
            response = get_fetch(URL_SERV + cat_route, PARAMS)
            response_data = response.json()['data']
            category_url = response_data['activeElementSlug']

            category_groups = response_data['body']

            for sub_cat in category_groups:
                sub_category_name = sub_cat['data']['title']
                products = sub_cat['data']['elements']

                page_num = 1
                category_full_path = self.categorie_dict['title'] + '/' + category_name + '/' + sub_category_name
                print(f'Glovo - запрос {page_num} из {len(self.categories)} по {category_full_path}')

                for product in products:

                    product_name = product['data']['name']
                    l = {
                        'mercant_id': MERCANTS['glv'],
                        'mercant_name': 'glv',
                        'product_id': product['data']['id'],
                        'title': product_name.replace("'", ''),
                        'description': '',
                        # здесь отсутствует url товара (карточки товара), по этому составим его
                        # из url категории (он существует) и id товара
                        'url': category_url + '_' + str(product['data']['id']),
                        'url_picture': product['data']['imageUrl'],
                        'time_scrap': str(datetime.datetime.now().isoformat()),
                        'sub_category': sub_category_name,
                        'category_full_path': category_full_path,
                        'brand': '',
                        'cost': product['data']['price'],
                        'prev_cost': 0
                    }

                    self.rezult.append(l) 

                page_num += 1 

            rand_pause()
            

    def __upload_to_db(self):
        upload_to_db(self.rezult, DB_PATH, DB_ROW_DATA_TABLE, DB_ROW_DATA_CREATE_STR, 'url')

    def start(self):
        self.fill_rezult()
        self.__upload_to_db()


def main():

    next_caterory_dct = get_next_categoy_glv(DB_PATH, DB_GLV_CATEGORY_TABLE, DB_GLV_CATEGORY_CREATE_STR, 'slug')

    glovo = GlovoApiScraper(next_caterory_dct)
    glovo.start()




if __name__ == '__main__':
    main()
