
############################### Получение токена
URL_TOKEN = 'https://mgo-gw2.e-magnum.kz/auth/server/api/v1/security/guest/login'

PARAMS_TOKEN =  {
  "headers": {
    'user-agent': 'Dart/2.19 (dart:io)',
    'x-client-version': '4.1.6 (100402) [iOS-16.5]',
    'accept': 'application/json',
    'accept-encoding': 'gzip',
    'content-length': '0',
    'host': 'mgo-gw2.e-magnum.kz',
    'content-type': 'application/json',
    'Connection': 'close'
  },
  "method": "POST",
  "body": ""
}


############################### Основной запрос к каталогу
URL_CATALOG = 'https://mgo-gw1.e-magnum.kz/catalog/client/platformItemV2'

TOKEN = '@TOKEN@'
CATEGORY_ID = '@CATID@'
PAGE_ID = '@PAGEID@'

PARAMS_CATALOG = {
    "headers": {
        'user-agent': 'Dart/2.19 (dart:io)',
        'x-client-version': '4.1.6 (100402) [iOS-16.5]',
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'authorization': f'{TOKEN}',
        'host': 'mgo-gw1.e-magnum.kz',
        'content-type': 'application/json'
     },

    "params": {
        'platformId': '5002',
        'categoryIds': f'{CATEGORY_ID}',
        'categoryIds': 'sales',
        'sortOrder': 'DESC',
        'pageId': f'{PAGE_ID}',
        'pageSize': '20',        # почему-то константная величина, не отражает реального количества страниц
        'filterIds': ''
    },

    "method": "GET",
    "body": ""
}

############################### Запрос к иерархии категорий
URL_CATEGORY = 'https://mgo-gw1.e-magnum.kz/catalog/client/catalog'

PARENT_ID = '@PARENT_ID@'

PARAMS_CATEGORY = {
    "headers": {
        'user-agent': 'Dart/2.19 (dart:io)',
        'x-client-version': '4.1.6 (100402) [iOS-16.5]',
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'Authorization': '',
        'host': 'mgo-gw1.e-magnum.kz',
        'content-type': 'application/json',
        'Connection': 'close'
     },

    "params": {
        'includeChildNodes': 'true',
        'parentId': '',
        'platformId': '5002'
    },

    "method": "GET",
    "body": ""
}