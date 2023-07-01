from scr.airba_fetch import PAGE, CATALOG, WORKFLOW, URL_CATEGORY, PARAMS_CATEGORY, \
                                REQ_LIMIT, URL_CATALOG, PARAMS_CATALOG
import datetime
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db, table_exists, get_next_categoy_list_mgm, \
                                update_category_mgm, update_parent_category_mgm
from constants.constants import DB_PATH, DB_AIR_CATEGORY_TABLE, DB_AIR_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE


class AirbaScrapper():
    def __init__(self) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.category_update = []
        self.workflow = WORKFLOW
    
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


    def start(self):
        self.fill_category_table()
        # self.fill_category_data()
        # self.__upload_to_db()


def main():
    airba = AirbaScrapper()
    airba.start()


if __name__ == '__main__':
    main()


