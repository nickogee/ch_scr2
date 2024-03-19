
############################### Получение токена
URL_TOKEN = 'https://authentication.wolt.com/v1/wauth2/access_token'
REFRESH_TOKEN_MASK = '@RT_MASK@'
PARAMS_TOKEN =  {
  "headers": {
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'clientversionnumber': '34900',
    'app-locale': 'ru-KZ',
    'app-language': 'ru',
    'client-version': '3.49.0',
    'accept-language': 'ru-KZ;q=1.00,kk-KZ;q=0.50',
    'accept-encoding': 'gzip, deflate, br',
    'x-wolt-visitor-id': 'EBE02D7C-B413-4B82-ACBB-6914041201A3',
    'platform': 'iPhone',
    'content-length': '110',
    'user-agent': 'Wolt/34900; Build/8818; iOS/16.6.1; iPhone; ru'
  },
  "method": "POST",
  "body": f"refresh_token={REFRESH_TOKEN_MASK}&grant_type=refresh_token&audience=restaurant-api"
}


############################### Основной запрос к каталогу
CURRENT_CATEGORY_MASK = '@CAT_MASK@'
URL_CATALOG = f'https://restaurant-api.wolt.com/v4/venues/63443c821dd17f940c4360fa/menu/categories/{CURRENT_CATEGORY_MASK}?language=ru&show_subcategories=true&unit_prices=true&show_weighted_items=true'

PARAMS_CATALOG = {
    "headers": {
        'method': 'GET',
        'scheme': 'https',
        'path': f'/v4/venues/63443c821dd17f940c4360fa/menu/categories/{CURRENT_CATEGORY_MASK}?language=ru&unit_prices=true&show_subcategories=true&show_weighted_items=true',
        'authority': 'restaurant-api.wolt.com',
        'authorization': '', 
        'accept': '*/*',
        'app-language': 'ru',
        'app-locale': 'ru-KZ',
        'clientversionnumber': '34900',
        'client-version': '3.49.0',
        'accept-language': 'ru-KZ;q=1.00,kk-KZ;q=0.50',
        'accept-encoding': 'gzip, deflate, br',
        'x-wolt-visitor-id': 'EBE02D7C-B413-4B82-ACBB-6914041201A3',
        'w-wolt-session-id': '1848DA4B-55DB-4593-BF98-2E309C38D53C',
        'platform': 'iPhone',
        'user-agent': 'Wolt/34900; Build/8818; iOS/16.6.1; iPhone; ru',
        'userlocationlng': '76.865025',
        'userlocationlat': '43.243218'
     },

    "params": {
        'language': 'ru',
        'unit_prices': 'true',
        'show_subcategories': 'true',
        'show_weighted_items': 'true',
    },

    "method": "GET",
    "body": ""
}

############################### Запрос к иерархии категорий
URL_CATEGORY = 'https://restaurant-api.wolt.com/v4/venues/63443c821dd17f940c4360fa/menu/data?unit_prices=true&show_weighted_items=true&show_subcategories=true'

PARAMS_CATEGORY = {
    "headers": {
        'method': 'GET',
        'scheme': 'https',
        'path': '/v4/venues/63443c821dd17f940c4360fa/menu/data?unit_prices=true&show_weighted_items=true&show_subcategories=true',
        'authority': 'restaurant-api.wolt.com',
        'authorization': '', 
        'accept': '*/*',
        'app-language': 'ru',
        'app-locale': 'ru-KZ',
        'clientversionnumber': '34900',
        'client-version': '3.49.0',
        'accept-language': 'ru-KZ;q=1.00,kk-KZ;q=0.50',
        'accept-encoding': 'gzip, deflate, br',
        'x-wolt-visitor-id': 'EBE02D7C-B413-4B82-ACBB-6914041201A3',
        'w-wolt-session-id': '1848DA4B-55DB-4593-BF98-2E309C38D53C',
        'platform': 'iPhone',
        'user-agent': 'Wolt/34900; Build/8818; iOS/16.6.1; iPhone; ru',
        'userlocationlng': '76.865025',
        'userlocationlat': '43.243218'
     },

    "params": {
        'unit_prices': 'true',
        'show_subcategories': 'true',
        'show_weighted_items': 'true',
    },

    "method": "GET",
    "body": ""
}