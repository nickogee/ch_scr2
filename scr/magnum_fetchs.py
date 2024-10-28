
############################### Получение токена
URL_TOKEN = 'https://mgo-gw2.e-magnum.kz/auth/server/api/v1/security/guest/login'

PARAMS_TOKEN =  {
  "headers": {
    'user-agent': 'Dart/2.19 (dart:io)',
    'x-client-version': '4.2.0 (100448) [iOS-17.4.1]',
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
REQ_LIMIT = 30  # лимит запросов на каждый запуск скрипта

PARAMS_CATALOG = {
    "headers": {
        'user-agent': 'Dart/2.19 (dart:io)',
        'x-client-version': '4.2.0 (100448) [iOS-17.4.1]',
        'accept': 'application/json',
        'accept-encoding': 'gzip',
        'Authorization': '',
        'host': 'mgo-gw1.e-magnum.kz',
        'content-type': 'application/json'
     },

    "params": {
        'platformId': '5002',
        'categoryIds': '',
        'sortTypeColumn': 'sales',
        'sortOrder': 'DESC',
        'pageId': '',
        'pageSize': '20',  # почему-то константная величина, не отражает реального количества страниц
        'filterIds': ''
    },

    "method": "GET",
    "body": ""
}

############################### Запрос к иерархии категорий
URL_CATEGORY = 'https://mgo-gw1.e-magnum.kz/catalog/client/catalog'

PARAMS_CATEGORY = {
    "headers": {
        'user-agent': 'Dart/2.19 (dart:io)',
        'x-client-version': '4.2.0 (100448) [iOS-17.4.1]',
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

CITYS_PLATFORM_ID = {'almaty': '5002',
                    'astana': '6002',
                    # 'shymkent': '7001'
                    }
    