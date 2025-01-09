from pathlib import Path


DIR = Path(__file__).resolve().parent.parent

MERCANTS = {
    'mgm_e-ala': '2d91243f-ceb9-4ada-a19a-ced9bd8a6b5b',
    'mgm-ala': '24c85cdd-cff6-4e60-a32c-e2193d08f964',
    'mgm-ast': '8ee8ee38-5732-411b-9e62-228303a8de6f',
    'air-ala': 'edf30565-d0d9-40ec-9759-6fde57220037',
    'glv-ala': 'cef9c961-c2e7-4d8a-9312-4d06b9fe8866',
    'abz-ala': '8bfdb88d-c8cc-4c2f-a363-e545296066b8',
    'abz-ast': 'e6af75c8-3f21-4bd0-8e74-184451d2ce26',
    'vlt-ala': '70e6a58b-bf0a-4d53-b2b8-af4e0399047f',
    'kvr-ast': '0b05ce6b-e701-4938-996b-726dbc541ebc',
    'lvk-ala': 'a1aef55b-dc0b-4ade-9377-8c7b2987d230',
}

CITY_POSTFIX = {
    'almaty': 'ala',
    'astana': 'ast',
}

UPLOAD_FOLDER = f'{DIR}/uploads/'


################################## SQLite ##################################
CITYS_LS = ['almaty', 'astana']

DB_PATH = f'{DIR}/db/scr_data.db'

DB_ROW_DATA_COLUMNS_LS = ['mercant_id', 
                          'mercant_name', 
                          'product_id', 
                          'id', 
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
                        id TEXT, 
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
                        id TEXT,
                        name TEXT,
                        category_lvl TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT,
                        key_column TEXT PRIMARY KEY
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

DB_KVR_CATEGORY_TABLE = 'kvr_category'
DB_KVR_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_KVR_CATEGORY_TABLE}(
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT
                        ) 
                    '''

DB_LVK_CATEGORY_TABLE = 'lvk_category'
DB_LVK_CATEGORY_CREATE_STR = f'''
                        CREATE TABLE IF NOT EXISTS {DB_LVK_CATEGORY_TABLE}(
                        sub_category_id TEXT,
                        category_id TEXT,
                        sub_category_name TEXT,
                        category_name TEXT,
                        sub_categoty_href TEXT,
                        scrap_count INTEGER DEFAULT 0,
                        city TEXT,
                        key_column TEXT PRIMARY KEY
                        ) 
                    '''