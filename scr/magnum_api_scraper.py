from scr.magnum_fetchs import PARAMS_TOKEN, URL_TOKEN, URL_CATEGORY, PARAMS_CATEGORY, PARENT_ID
import datetime
from scr.share_functions import get_fetch, rand_pause
from scr.database_worker import upload_to_db
from constants.constants import DB_PATH, DB_MGM_CATEGORY_TABLE, DB_MGM_CATEGORY_CREATE_STR


class MagnumScrapper():
    def __init__(self) -> None:
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.category_list = []
        self.token = None
        self.token = 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3OTk5Nzc3Nzc3NyIsImF1ZCI6ImNpdHJvLXNlcnZpY2VzIiwic2NvcGUiOlsiNCIsIjgiXSwiaXNzIjoiaHR0cHM6XC9cL2NpdHJvYnl0ZS5jb20iLCJleHAiOjE2ODc1NTQ1NDYsInVzZXJJZCI6NjU1MzI0LCJpYXQiOjE2ODc1MTg1NDYsImp0aSI6ImRmYjE3Y2ViLTdmNWMtNGIyNS1iMzIyLTZhMDk2ZTYzOGUxMSJ9.J4g4ztBHXRq3r9bNUzD-InlDQ8FoB6otVPbjvNZexJJq2TeoP_m-S81YeLNgv_GHKQCo6KQdXuD_A3dUib-SD-M46BUvj4yzpnnc4JfEtCg_5FbOYhigb2d6bDlyaHflMqOuKqBiomxWCPGH2q4IsqW5gHoUc9d05o77-81ZTym5Whk3bR8TVqOYy-4Vvy91HprpWyVEu6ECGg0uEEPsxUSYPO9Wiy9NohokIRAyeqc6rs8m_8KLfrbKGuR17k86h5Xjr_Or8IhFsbXqSShdU3KPkuywPQR5qWjawgjoUhXzJvNv83CcaVofhAvxfwx83TqSvTtKgDrGcxOEjj6JXg'
        self.get_token()
        

    
    def get_token(self):
        if not self.token:
            resp = get_fetch(url=URL_TOKEN, params=PARAMS_TOKEN)
            resp_js = resp.json()
            
            if resp_js['token']:
                self.token = resp_js['token']
    

    def fill_category_table(self):
        
        # для самого верхнего уровня категорий PARENT_ID пустой
        params_head = PARAMS_CATEGORY.copy()
        params_head['params']['parentId'] = ''
        params_head['headers']['Authorization'] = self.token
         
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
            }

            print(f"Получаем категорию id={head_dct['id']}, name={head_dct['name']}")
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
                            }
                    
                    print(f"Получаем категорию id={chld_dct['id']}, name={chld_dct['name']}")
                    self.category_list.append(dct)

                    rand_pause()

                    # для каждой категории второго уровня делаем запрос, чтобы получить дочерние категории (3-го уровня)
                    params_chld = PARAMS_CATEGORY.copy()
                    params_chld['params']['parentId'] = str(chld_dct['parentId'])
                    params_chld['headers']['Authorization'] = self.token
                    
                    chld_resp = get_fetch(url=URL_CATEGORY, params=params_chld)
                    chld_resp_js = chld_resp.json()

                    for i in chld_resp_js:
                        # здесь нудны только дочерние элементы
                        sub_chld_ls = i.get('childCategories')
                        if sub_chld_ls:
                            for sub_chld_dct in sub_chld_ls:
                                
                                # добавляем категорию третьего уровня
                                dct = {
                                'parent_id': str(sub_chld_dct['parentId']),
                                'id': str(sub_chld_dct['id']),
                                'name': str(sub_chld_dct['name']),
                                'category_lvl': '3',
                                        }

                                print(f"Получаем категорию id={sub_chld_dct['id']}, name={sub_chld_dct['name']}")
                                self.category_list.append(dct)


        if self.category_list:
            upload_to_db(rezult=self.category_list, 
                        db_path=DB_PATH, 
                        table_name=DB_MGM_CATEGORY_TABLE,
                        table_create_str=DB_MGM_CATEGORY_CREATE_STR,
                        pk_column='id')

            



def main():
    magnum = MagnumScrapper()
    magnum.fill_category_table()
    d = 1




if __name__ == '__main__':
    main()
