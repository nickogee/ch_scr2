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
            sql_txt = f'''SELECT count(name) FROM sqlite_schema WHERE TYPE = 'table' AND name = '{self.table_name}' '''
            self.cursor.execute(sql_txt) 
            return (self.cursor.fetchone()[0] == 1)
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return True
        
    
    
    def crate_table(self):

        if not self.table_exists():
            try: 
                self.cursor.execute(self.table_create_str)
            except Exception as ex:
                print('Не удалось выполнить запрос:', self.table_create_str, f'По причине: {ex}', sep='\n')
    

    def data_exists(self, product_dict:dict):
        try:
            sql_txt = f'''SELECT {self.pk_column} FROM {self.table_name} WHERE {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}'''
            self.cursor.execute(sql_txt)
            return bool(self.cursor.fetchall())
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return False

    def insert_data(self, product_dict:dict):

        keys_ls = [key for key in product_dict.keys()]
        keys_str = ', '.join(keys_ls)
        param_ls = ['?' for key in product_dict.keys()]
        param_str = ', '.join(param_ls)

        try:
            sql_txt = f'''INSERT INTO {self.table_name} ({keys_str}) VALUES({param_str}) '''
            self.cursor.execute(sql_txt, tuple(product_dict.values())) 
            self.connect.commit()
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')

    def update_data(self, product_dict:dict):
        sql_txt = ''
        items_ls = []
        for key, val in product_dict.items():

            if isinstance(val, float) or isinstance(val, int):
                st = str(key) + ' = ' + str(val)
            else:
                st = str(key) + ' = ' + "'" + str(val) + "'"

            items_ls.append(st)

        items_str = ', '.join(items_ls)
        try:
            sql_txt = f'''UPDATE {self.table_name} SET {items_str} WHERE  {self.pk_column} = {"'" + product_dict[self.pk_column] + "'"}'''
            self.cursor.execute(sql_txt)
            self.connect.commit()
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
     

    def insert_update_data(self, rezult:list):
        for product_dict in rezult:

            if self.data_exists(product_dict):
                self.update_data(product_dict)
            else:
                self.insert_data(product_dict)
    

    def get_next_category_glv(self, order_by:str):
        try:
            sql_txt = f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1'''
            result = self.cursor.execute(sql_txt).fetchone()
            result_dct = {
                    'title': result[0],
                    'slug': result[1],
                    'scrap_count': result[2],
                    }
            return result_dct
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None
    
    def get_next_category_abz(self, order_by:str):
        try:
            sql_txt = f'''SELECT * FROM {self.table_name} ORDER BY {order_by} LIMIT 1'''
            result = self.cursor.execute(sql_txt).fetchone()
            result_dct = {
                    'title': result[0],
                    'href': result[1],
                    'catalog': result[2],
                    'scrap_count': result[3],
                    }
            return result_dct
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None

    def get_next_category_list_mgm_air(self, mercant:str, last_lvl:str):

        # Получим список из id категорий last_lvl + 1 уровня, 
        # у которых parent_id имеет имнимальное значение scrap_count из всех категорий last_lvl уровня.
        # Отсортируем их по возростанию scrap_count, чтобы первыми соберать самые "давние" подкатегории 
        sql_txt = f'''
                SELECT
                    lvl.id as id,
                    lvl.name as name,
                    lvl_2.name as parent_name,
                    lvl_3.name as head_parent_name,
                    lvl.scrap_count as scrap_count,
                    lvl_2.scrap_count as scrap_count_parent,
                    lvl_2.id as parent1_id,
                    lvl_3.id as parent2_id,
                    lvl_3.parent_id as parent3_id
                FROM 
                    {mercant}_category as lvl
                INNER JOIN {mercant}_category as lvl_2 
                ON lvl.parent_id = lvl_2.id
                INNER JOIN {mercant}_category as lvl_3 
                ON lvl_2.parent_id = lvl_3.id
                WHERE lvl.parent_id IN 
                    (SELECT 
                        mc.id
                    FROM {mercant}_category mc
                    WHERE mc.category_lvl = '{last_lvl}'
                    ORDER BY mc.scrap_count 
                    LIMIT 2
                    )
                ORDER BY lvl.scrap_count   
                '''

        try:  
            result = self.cursor.execute(sql_txt).fetchall()
            return result
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None
    

    def get_next_category_vlt(self, order_by:str, fast_category_id):
        
        if fast_category_id:
            condition = f"WHERE id = '{fast_category_id}'"
        else:
            condition = "WHERE id <> '63443f7efed9bfd239e95b30'"
           

        try:
            sql_txt = f'''SELECT * FROM {self.table_name} {condition} ORDER BY {order_by} LIMIT 1'''
            result = self.cursor.execute(sql_txt).fetchone()
            result_dct = {
                    'id': result[0],
                    'name': result[1],
                    'scrap_count': result[2],
                    }
            return result_dct
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None
        

    def get_category_list_mgm_air(self, mercant:str, last_lvl:str, fast_category_id):

        # Получим список из id категорий last_lvl + 1 уровня, 
        # у которых parent_id имеет имнимальное значение scrap_count из всех категорий last_lvl уровня.
        # (для "быстрого парсера" по нужной категории)
        # Отсортируем их по возростанию scrap_count, чтобы первыми соберать самые "давние" подкатегории 
        if fast_category_id:
            fast_category_str = f"AND mc.id = '{fast_category_id}'"
        else:
            fast_category_str = ''

        sql_txt = f'''
                SELECT
                    lvl.id as id,
                    lvl.name as name,
                    lvl_2.name as parent_name,
                    lvl_3.name as head_parent_name,
                    lvl.scrap_count as scrap_count,
                    lvl_2.scrap_count as scrap_count_parent,
                    lvl_2.id as parent1_id,
                    lvl_3.id as parent2_id,
                    lvl_3.parent_id as parent3_id
                FROM 
                    {mercant}_category as lvl
                INNER JOIN {mercant}_category as lvl_2 
                ON lvl.parent_id = lvl_2.id
                INNER JOIN {mercant}_category as lvl_3 
                ON lvl_2.parent_id = lvl_3.id
                WHERE lvl.parent_id IN 
                    (SELECT 
                        mc.id
                    FROM {mercant}_category mc
                    WHERE mc.category_lvl = '{last_lvl}' {fast_category_str}
                    ORDER BY mc.scrap_count 
                    LIMIT 2
                    )
                ORDER BY lvl.scrap_count   
                '''

        try:  
            result = self.cursor.execute(sql_txt).fetchall()
            return result
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None
    

    def get_data(self, columns: str, filter_tpl: tuple):

        try:
            if filter_tpl:
                sql_txt = f'''SELECT {columns} FROM {self.table_name} WHERE {filter_tpl[0]} = {"'" + filter_tpl[1] + "'"}'''
            else:
                sql_txt = f'''SELECT {columns} FROM {self.table_name}'''

            result = self.cursor.execute(sql_txt)
            return result
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return None
        
    def truncate_table(self):
        sql_txt = f'DELETE FROM {self.table_name};'
        try:
            result = self.cursor.execute(sql_txt)
            self.connect.commit()
            return True
        except Exception as ex:
            print('Не удалось выполнить запрос:', sql_txt, f'По причине: {ex}', sep='\n')
            return False

    
    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as ex:
            print(f'Не удалось закрыть соединение с БД по причине: {ex}')



def upload_to_db(rezult, db_path, table_name, table_create_str, pk_column):
    
    db_ses = DBSqlite(db_path, table_name, table_create_str, pk_column)
    db_ses.crate_table()
    db_ses.insert_update_data(rezult)


def get_data_from(db_path, table_name, columns: str, filter_tpl: tuple):
    db_ses = DBSqlite(db_path, table_name, None, None)
    result_ls = db_ses.get_data(columns=columns, filter_tpl=filter_tpl).fetchall()
    return result_ls


def truncate_table(db_path, table_name: str):
    db_ses = DBSqlite(db_path, table_name, None, None)
    return db_ses.truncate_table()


def create_table(db_path, table_name, table_create_str):
    db_ses = DBSqlite(db_path, table_name, table_create_str, None)
    db_ses.crate_table()


# --------------------- Volt --------------------
def get_next_categoy_vlt(db_path, table_name, pk_column, fast_category_ls):
    
    db_ses = DBSqlite(db_path, table_name, table_create_str=None, pk_column=pk_column)
    ls = []
    if fast_category_ls:
        for current_cat in fast_category_ls:
            result_dct = db_ses.get_next_category_vlt(order_by='scrap_count', fast_category_id=current_cat)
            ls.append(result_dct)

            result_dct_to_update = result_dct.copy()
            result_dct_to_update['scrap_count'] += 1
            db_ses.update_data(result_dct_to_update)
    else:
        result_dct = db_ses.get_next_category_vlt(order_by='scrap_count', fast_category_id=None)
        ls.append(result_dct)

        result_dct_to_update = result_dct.copy()
        result_dct_to_update['scrap_count'] += 1
        db_ses.update_data(result_dct_to_update)


    return ls   

# --------------------- Glovo --------------------
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


# --------------------- Arbuz --------------------
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
            

# --------------------- Magnum + Airba --------------------
def get_next_categoy_list_mgm_air(db_path, table_name, mercant:str, cat_lvl:str, fast_category_id):
    '''получает список категорий 3-го уровня, по которым нужно соберать данные'''

    db_ses = DBSqlite(db_path, table_name, '', '') 
    # result_ls = db_ses.get_next_category_list_mgm_air(mercant, cat_lvl)
    result_ls = db_ses.get_category_list_mgm_air(mercant, cat_lvl, fast_category_id)
    return result_ls

def update_category_mgm_air(update_ls, db_path, table_name, pk_column):
    db_ses = DBSqlite(db_path, table_name, '', pk_column)
    for cat_dct in update_ls:
        db_ses.update_data(cat_dct)

def update_parent_category_mgm_air(db_path, table_name, pk_column, filter_tpl): 
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

# --------------------- XML --------------------
def read_mercant_data(db_path, table_name, columns, filter_tpl):
    db_ses = DBSqlite(db_path, table_name, None, None)
    result_ls = db_ses.get_data(columns=columns, filter_tpl=filter_tpl).fetchall()
    return result_ls


def table_exists(db_path, table_name):
    db_ses = DBSqlite(db_path=db_path, table_name=table_name, table_create_str=None, pk_column=None)
    return db_ses.table_exists()





