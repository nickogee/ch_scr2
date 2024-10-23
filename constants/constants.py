from pathlib import Path


DIR = Path(__file__).resolve().parent.parent


MERCANTS = {
    'mgm_e': '2d91243f-ceb9-4ada-a19a-ced9bd8a6b5b',
    'mgm': '24c85cdd-cff6-4e60-a32c-e2193d08f964',
    'air': 'edf30565-d0d9-40ec-9759-6fde57220037',
    'glv': 'cef9c961-c2e7-4d8a-9312-4d06b9fe8866',
    'abz': '8bfdb88d-c8cc-4c2f-a363-e545296066b8',
    'vlt': '70e6a58b-bf0a-4d53-b2b8-af4e0399047f'
}

UPLOAD_FOLDER = f'{DIR}/uploads/'


################################## SQLite ##################################
CITYS_LS = ['almaty', 'astana']
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
                          'measure',
                          'city',
                          ]

DB_ROW_DATA_TABLE = 'row_data'
DB_ROW_DATA_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_ROW_DATA_TABLE}( 
                        mercant_id TEXT, 
                        mercant_name TEXT, 
                        product_id TEXT PRIMARY KEY, 
                        title TEXT, 
                        cost INTEGER DEFAULT 0, 
                        prev_cost INTEGER DEFAULT 0, 
                        description TEXT, 
                        url TEXT, 
                        url_picture TEXT, 
                        category_full_path TEXT, 
                        brand TEXT, 
                        sub_category TEXT, 
                        time_scrap TEXT,
                        measure TEXT,
                        city TEXT
                        )
                    '''


DB_GLV_CATEGORY_TABLE = 'glv_category'
DB_GLV_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_GLV_CATEGORY_TABLE}( 
                        title TEXT, 
                        slug TEXT PRIMARY KEY,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_ABZ_CATEGORY_TABLE = 'abz_category'
DB_ABZ_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_ABZ_CATEGORY_TABLE}( 
                        title TEXT, 
                        href TEXT PRIMARY KEY,
                        catalog TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_MGM_CATEGORY_TABLE = 'mgm_category'
DB_MGM_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_MGM_CATEGORY_TABLE}( 
                        parent_id TEXT, 
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        category_lvl TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_MGM_E_CATEGORY_TABLE = 'mgm_e_category'
DB_MGM_E_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_MGM_E_CATEGORY_TABLE}( 
                        parent_id TEXT, 
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        category_lvl TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_AIR_CATEGORY_TABLE = 'air_category'
DB_AIR_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_AIR_CATEGORY_TABLE}( 
                        parent_id TEXT, 
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        category_lvl TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_VLT_CATEGORY_TABLE = 'vlt_category'
DB_VLT_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_VLT_CATEGORY_TABLE}(
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_VLT_REFRESH_TOKEN_TABLE = 'vlt_refresh_token'
DB_VLT_REFRESH_TOKEN_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_VLT_REFRESH_TOKEN_TABLE}( 
                        refresh_token TEXT PRIMARY KEY
                        ) 
                    '''