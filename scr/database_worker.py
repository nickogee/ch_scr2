import sqlite3 
from scr.glovo_fetchs import CATEGORIES_GLV
from scr.arbuz_fetchs import CATEGORIES_ABZ
# from scr.magnum_fetchs import CATEGORIES_M




class DBSqlite():
    
    def __init__(self, db_path, table_name, table_create_str, pk_column) -> None:
        conn = sqlite3.connect(db_path)
        self.connect = conn 
        self.cursor = conn.cursor()
        self.table_name = table_name
        self.table_create_str = table_create_str
        self.pk_column = pk_column

    def table_exists(self): 
        self.cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{self.table_name}' ''') 
        if self.cursor.fetchone()[0] == 1: 
            return True 
        return False
    
    def crate_table(self):

        if not self.table_exists(): 
            self.cursor.execute(self.table_create_str)
    

    def data_exists(self, product_dict:dict):
        self.cursor.execute(f'''SELECT {self.pk_column} FROM {self.table_name} WHERE {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}''')
        return bool(self.cursor.fetchall())

    def insert_data(self, product_dict:dict):

        keys_ls = [key for key in product_dict.keys()]
        keys_str = ', '.join(keys_ls)
        param_ls = ['?' for key in product_dict.keys()]
        param_str = ', '.join(param_ls)

        self.cursor.execute(f'''INSERT INTO {self.table_name} ({keys_str}) VALUES({param_str}) ''',
                             tuple(product_dict.values())) 
        self.connect.commit()

    def update_data(self, product_dict:dict):

        items_ls = []
        for key, val in product_dict.items():

            if isinstance(val, float) or isinstance(val, int):
                st = str(key) + ' = ' + str(val)
            else:
                st = str(key) + ' = ' + "'" + str(val) + "'"

            items_ls.append(st)

        items_str = ', '.join(items_ls)
        self.cursor.execute(f'''UPDATE {self.table_name} SET {items_str} WHERE  {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}''')
        self.connect.commit()
     

    def insert_update_data(self, rezult:list):
        for product_dict in rezult:

            if self.data_exists(product_dict):
                self.update_data(product_dict)
            else:
                self.insert_data(product_dict)
    

    def get_next_category_glv(self, order_by:str):
        result = self.cursor.execute(f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1''').fetchone()
        result_dct = {
                'title': result[0],
                'slug': result[1],
                'scrap_count': result[2],
                  }
        return result_dct
    
    def get_next_category_abz(self, order_by:str):
        result = self.cursor.execute(f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1''').fetchone()
        result_dct = {
                'title': result[0],
                'href': result[1],
                'catalog': result[2],
                'scrap_count': result[3],
                  }
        return result_dct


    def get_data(self, columns: str, filter_tpl: tuple):
        result = self.cursor.execute(f'''SELECT {columns} FROM {self.table_name} WHERE {filter_tpl[0]} = {"'" + filter_tpl[1] + "'"}''')
        return result

    def __del__(self):
        self.cursor.close()
        self.connect.close()





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
            

def read_mercant_data(db_path, table_name, columns, filter_tpl):
    db_ses = DBSqlite(db_path, table_name, None, None)
    result_ls = db_ses.get_data(columns=columns, filter_tpl=filter_tpl).fetchall()
    return result_ls







