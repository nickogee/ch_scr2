


############################### Запрос к иерархии категорий
URL_CATEGORY = 'https://food-catalog.clevermarket.kz/api/mobile/1.0/catalog/catalogs'

PARAMS_CATEGORY = {
    "headers": {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
  },

    "params": {
        "referrer": "https://clevermarket.kz/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": None,
        "method": "GET",
        "mode": "cors",
        "credentials": "omit"
    },

    "method": "GET",
    "body": ""
}


############################### Основной запрос к каталогу
URL_CATALOG = 'https://food-catalog.clevermarket.kz/api/mobile/3.0/catalog/get-by-catalog-id'
REQ_LIMIT = 30  # лимит запросов на каждый запуск скрипта
CATALOG = '@CAT@'
PAGE = '@PAGE@'


PARAMS_CATALOG = {
    "headers": {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
  },

    "params": {
        'CatalogId': CATALOG,
        'pageSize': '10',
        'pageNumber': str(PAGE),
        'PriceOrderBy': 'Default',
        'referrer': 'https://clevermarket.kz/',
        'referrerPolicy': 'strict-origin-when-cross-origin',
        'mode': 'cors',
        'credentials': 'omit',
    },

    "method": "GET",
    "body": ""
}
