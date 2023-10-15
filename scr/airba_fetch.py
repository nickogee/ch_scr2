
# WORKFLOW = '28f8d037-3499-4186-9e08-6a2c4ae48cf6'
WORKFLOW = '25882eb0-327c-4b7c-92d7-6ae5d8fafbe7'

############################### Запрос к иерархии категорий
URL_CATEGORY = 'https://backend.airbafresh.kz/api/nomenclature/catalog-tree/'

PARAMS_CATEGORY = {
    "headers": {
        'method': 'GET',
        'scheme': 'https',
        'path': '/api/nomenclature/catalog-tree/',
        'authority': 'backend.airbafresh.kz',
        'accept': '*/*',
        'content-type': 'application/json',
        'app-version': '1.0.30',
        'accept-encoding': 'gzip, deflate, br',
        'app-platform': 'iOS',
        'language': 'ru',
        'user-agent': 'Airba%20Fresh/2 CFNetwork/1410.0.3 Darwin/22.6.0',
        'accept-language': 'ru',
        'workflow': WORKFLOW,
        'mindbox-device-uuid': 'A961E0CE-70C1-41F0-8BF2-FC0E31B1A85F',
        # 'Host': 'backend.airbafresh.kz',
        # 'Connection': 'close'

     },

    "params": {
        
    },

    "method": "GET",
    "body": ""
}


############################### Основной запрос к каталогу
URL_CATALOG = 'https://backend.airbafresh.kz/api/nomenclature/catalog'
REQ_LIMIT = 30  # лимит запросов на каждый запуск скрипта
CATALOG = '@CAT@'
PAGE = '@PAGE@'


PARAMS_CATALOG = {
    "headers": {
        'method': 'GET',
        'scheme': 'https',
        'path': f'/api/nomenclature/catalog?category={CATALOG}&search_term=&page={str(PAGE)}&count=20&sort_by=default',
        'authority': 'backend.airbafresh.kz',
        'accept': '*/*',
        'content-type': 'application/json',
        'app-version': '1.0.30',
        'accept-encoding': 'gzip, deflate, br',
        'app-platform': 'iOS',
        'language': 'ru',
        'user-agent': 'Airba%20Fresh/2 CFNetwork/1410.0.3 Darwin/22.6.0',
        'accept-language': 'ru',
        'workflow': WORKFLOW,
        'mindbox-device-uuid': 'A961E0CE-70C1-41F0-8BF2-FC0E31B1A85F',
        # 'Host': 'backend.airbafresh.kz',
        # 'Connection': 'close'

     },

    "params": {
        'category': CATALOG,
        'search_term': '',
        'page': str(PAGE),
        'count': '20',  # почему-то константная величина, не отражает реального количества страниц
        'sort_by': 'default'
    },

    "method": "GET",
    "body": ""
}
