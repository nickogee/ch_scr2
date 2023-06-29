import sqlite3 
from scr.glovo_fetchs import CATEGORIES_GLV
from scr.arbuz_fetchs import CATEGORIES_ABZ




class DBSqlite():
    
    def __init__(self, db_path, table_name, table_create_str, pk_column) -> None:
        conn = sqlite3.connect(db_path)
        self.connect = conn 
        self.cursor = conn.cursor()
        self.table_name = table_name
        self.table_create_str = table_create_str
        self.pk_column = pk_column

    def table_exists(self): 

        try:
            self.cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{self.table_name}' ''') 
            return (self.cursor.fetchone()[0] == 1)
        except Exception as ex:
            print(ex)
            return True
        
    
    
    def crate_table(self):

        if not self.table_exists():
            try: 
                self.cursor.execute(self.table_create_str)
            except Exception as ex:
                print(ex)
    

    def data_exists(self, product_dict:dict):
        try:
            self.cursor.execute(f'''SELECT {self.pk_column} FROM {self.table_name} WHERE {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}''')
            return bool(self.cursor.fetchall())
        except Exception as ex:
            print(ex)
            return False

    def insert_data(self, product_dict:dict):

        keys_ls = [key for key in product_dict.keys()]
        keys_str = ', '.join(keys_ls)
        param_ls = ['?' for key in product_dict.keys()]
        param_str = ', '.join(param_ls)

        try:
            self.cursor.execute(f'''INSERT INTO {self.table_name} ({keys_str}) VALUES({param_str}) ''',
                                tuple(product_dict.values())) 
            self.connect.commit()
        except Exception as ex:
            print(ex)

    def update_data(self, product_dict:dict):

        items_ls = []
        for key, val in product_dict.items():

            if isinstance(val, float) or isinstance(val, int):
                st = str(key) + ' = ' + str(val)
            else:
                st = str(key) + ' = ' + "'" + str(val) + "'"

            items_ls.append(st)

        items_str = ', '.join(items_ls)
        try:
            self.cursor.execute(f'''UPDATE {self.table_name} SET {items_str} WHERE  {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}''')
            self.connect.commit()
        except Exception as ex:
            print(ex)
     

    def insert_update_data(self, rezult:list):
        for product_dict in rezult:

            if self.data_exists(product_dict):
                self.update_data(product_dict)
            else:
                self.insert_data(product_dict)
    

    def get_next_category_glv(self, order_by:str):
        try:
            result = self.cursor.execute(f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1''').fetchone()
            result_dct = {
                    'title': result[0],
                    'slug': result[1],
                    'scrap_count': result[2],
                    }
            return result_dct
        except Exception as ex:
            print(ex)
            return None
    
    def get_next_category_abz(self, order_by:str):
        try:
            result = self.cursor.execute(f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1''').fetchone()
            result_dct = {
                    'title': result[0],
                    'href': result[1],
                    'catalog': result[2],
                    'scrap_count': result[3],
                    }
            return result_dct
        except Exception as ex:
            print(ex)
            return None

    def get_next_category_list_mgm(self):

        # Получим список из id категорий 3-го уровня, 
        # у которых parent_id имеет имнимальное значение scrap_count из всех категорий 2-го уровня.
        # Отсортируем их по возростанию scrap_count, чтобы первыми соберать самые "давние" подкатегории 
        sql_txt = '''
                SELECT
                    mgm.id as id,
                    mgm.name as name,
                    mgm_2.name as parent_name,
                    mgm_3.name as head_parent_name,
                    mgm.scrap_count as scrap_count,
                    mgm_2.scrap_count as scrap_count_parent,
                    mgm.parent_id as parent_id
                FROM 
                    mgm_category as mgm
                INNER JOIN mgm_category as mgm_2 
                ON mgm.parent_id = mgm_2.id
                INNER JOIN mgm_category as mgm_3 
                ON mgm_2.parent_id = mgm_3.id
                WHERE mgm.parent_id IN 
                    (SELECT 
                        mc.id
                    FROM mgm_category mc
                    WHERE mc.category_lvl = '2'
                    ORDER BY mc.scrap_count 
                    LIMIT 1
                    )
                ORDER BY mgm.scrap_count   
                '''

        try:  
            result = self.cursor.execute(sql_txt).fetchall()
            return result
        except Exception as ex:
            print(ex)
            return None
    

    def get_data(self, columns: str, filter_tpl: tuple):
        try:
            result = self.cursor.execute(f'''SELECT {columns} FROM {self.table_name} WHERE {filter_tpl[0]} = {"'" + filter_tpl[1] + "'"}''')
            return result
        except Exception as ex:
            print(ex)
            return None

    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as ex:
            print(ex)





def upload_to_db(rezult, db_path, table_name, table_create_str, pk_column):
    
    db_ses = DBSqlite(db_path, table_name, table_create_str, pk_column)
    db_ses.crate_table()
    db_ses.insert_update_data(rezult)


def get_next_categoy_glv(db_path, table_name, table_create_str, pk_column):
    
    db_ses = DBSqlite(db_path, table_name, table_create_str, pk_column)
    # создадим и заполним таблицу категорий glv, если ее нет
    if not db_ses.table_exists():
        db_ses.crate_table()
        for cat_dict in CATEGORIES_GLV:
            db_ses.insert_data(cat_dict)

    result_dct = db_ses.get_next_category_glv('scrap_count')
    result_dct_to_update = result_dct.copy()
    result_dct_to_update['scrap_count'] += 1

    db_ses.update_data(result_dct_to_update)
    return result_dct


def get_next_categoy_abz(db_path, table_name, table_create_str, pk_column):
    
    db_ses = DBSqlite(db_path, table_name, table_create_str, pk_column)
    # создадим и заполним таблицу категорий glv, если ее нет
    if not db_ses.table_exists():
        db_ses.crate_table()
        for cat_dict in CATEGORIES_ABZ:
            db_ses.insert_data(cat_dict)

    result_dct = db_ses.get_next_category_abz('scrap_count')
    result_dct_to_update = result_dct.copy()
    result_dct_to_update['scrap_count'] += 1

    db_ses.update_data(result_dct_to_update)
    return result_dct
            

def get_next_categoy_list_mgm(db_path, table_name):
    '''получает список категорий 3-го уровня, по которым нужно соберать данные'''

    db_ses = DBSqlite(db_path, table_name, '', '') 
    result_ls = db_ses.get_next_category_list_mgm()
    return result_ls

def update_category_mgm(update_ls, db_path, table_name, pk_column):
    db_ses = DBSqlite(db_path, table_name, '', pk_column)
    for cat_dct in update_ls:
        db_ses.update_data(cat_dct)

def update_parent_category_mgm(db_path, table_name, pk_column, filter_tpl): 
    columns = 'scrap_count'
    db_ses = DBSqlite(db_path, table_name, None, pk_column)
    result_ls = db_ses.get_data(columns=columns, filter_tpl=filter_tpl).fetchall()
    sc_ls = [i[0] for i in result_ls]
    sc_min = min(sc_ls)

    cat_dct =   {
            'id': filter_tpl[1],
            'scrap_count': sc_min 
                }
    
    db_ses.update_data(cat_dct)

    

def read_mercant_data(db_path, table_name, columns, filter_tpl):
    db_ses = DBSqlite(db_path, table_name, None, None)
    result_ls = db_ses.get_data(columns=columns, filter_tpl=filter_tpl).fetchall()
    return result_ls


def table_exists(db_path, table_name):
    db_ses = DBSqlite(db_path=db_path, table_name=table_name, table_create_str=None, pk_column=None)
    return db_ses.table_exists()





