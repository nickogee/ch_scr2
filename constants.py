import os
from pathlib import Path


DIR = Path(__file__).resolve().parent


MERCANTS = {
    'mgm': '24c85cdd-cff6-4e60-a32c-e2193d08f964',
    'air': 'edf30565-d0d9-40ec-9759-6fde57220037',
    'glv': 'cef9c961-c2e7-4d8a-9312-4d06b9fe8866',
    'abz': '8bfdb88d-c8cc-4c2f-a363-e545296066b8'
}

UPLOAD_FOLDER = f'{DIR}/uploads/'


################################## SQLite ##################################

DB_PATH = f'{DIR}/db/scr_data.db'

DB_ROW_DATA_COLUMNS_LS = ['mercant_id', 
                          'mercant_name', 
                          'product_id', 
                          'title', 
                          'cost', 
                          'prev_cost', 
                          'description', 
                          'url',
                          'url_picture',
                          'category_full_path',
                          'brand',
                          'sub_category',
                          'time_scrap',
                          ]

DB_ROW_DATA_TABLE = 'row_data'
DB_ROW_DATA_CREATE_STR = f'''
                        CREATE TABLE {DB_ROW_DATA_TABLE}( 
                        mercant_id TEXT, 
                        mercant_name TEXT, 
                        product_id TEXT, 
                        title TEXT, 
                        cost INTEGER DEFAULT 0, 
                        prev_cost INTEGER DEFAULT 0, 
                        description TEXT, 
                        url TEXT PRIMARY KEY, 
                        url_picture TEXT, 
                        category_full_path TEXT, 
                        brand TEXT, 
                        sub_category TEXT, 
                        time_scrap TEXT
                        ) 
                    '''


DB_GLV_CATEGORY_TABLE = 'glv_category'
DB_GLV_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE {DB_GLV_CATEGORY_TABLE}( 
                        title TEXT, 
                        slug TEXT PRIMARY KEY,
                        scrap_count INTEGER DEFAULT 0
                        ) 
                    '''

DB_ABZ_CATEGORY_TABLE = 'abz_category'
DB_ABZ_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE {DB_ABZ_CATEGORY_TABLE}( 
                        title TEXT, 
                        href TEXT PRIMARY KEY,
                        catalog TEXT,
                        scrap_count INTEGER DEFAULT 0
                        ) 
                    '''