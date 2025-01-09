
############################### Получение токена
URL_TOKEN = 'https://lavka.yandex.kz/'
# REFRESH_TOKEN_MASK = '@RT_MASK@'
PARAMS_TOKEN =  {
  "headers": {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    'host': 'lavka.yandex.kz',
    'sec-ch-ua':'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests':'1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    
  },
  "body": None,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}


# ############################### Основной запрос к каталогу
# CURRENT_CATEGORY_MASK = '@CAT_MASK@'
# URL_CATALOG = f'https://restaurant-api.wolt.com/v4/venues/63443c821dd17f940c4360fa/menu/categories/{CURRENT_CATEGORY_MASK}?language=ru&show_subcategories=true&unit_prices=true&show_weighted_items=true'

# PARAMS_CATALOG = {
#     "headers": {
#         'method': 'GET',
#         'scheme': 'https',
#         'path': f'/v4/venues/63443c821dd17f940c4360fa/menu/categories/{CURRENT_CATEGORY_MASK}?language=ru&unit_prices=true&show_subcategories=true&show_weighted_items=true',
#         'authority': 'restaurant-api.wolt.com',
#         'authorization': '', 
#         'accept': '*/*',
#         'app-language': 'ru',
#         'app-locale': 'ru-KZ',
#         'clientversionnumber': '34900',
#         'client-version': '3.49.0',
#         'accept-language': 'ru-KZ;q=1.00,kk-KZ;q=0.50',
#         # 'accept-encoding': 'gzip, deflate, br',
#         'x-wolt-visitor-id': 'EBE02D7C-B413-4B82-ACBB-6914041201A3',
#         'w-wolt-session-id': '1848DA4B-55DB-4593-BF98-2E309C38D53C',
#         'platform': 'iPhone',
#         'user-agent': 'Wolt/34900; Build/8818; iOS/16.6.1; iPhone; ru',
#         'userlocationlng': '',
#         'userlocationlat': ''
#      },

#     "params": {
#         'language': 'ru',
#         'unit_prices': 'true',
#         'show_subcategories': 'true',
#         'show_weighted_items': 'true',
#     },

#     "method": "GET",
#     "body": ""
# }

# ############################### Запрос к иерархии категорий
# # URL_CATEGORY = 'https://restaurant-api.wolt.com/v4/venues/63443c821dd17f940c4360fa/menu/data?unit_prices=true&show_weighted_items=true&show_subcategories=true'
# URL_CATEGORY = 'https://restaurant-api.wolt.com/v4/venues/63443c821dd17f940c4360fa/menu/data?show_subcategories=true&show_weighted_items=true&show_fulfillment_lead_times=false&unit_prices=true'

# PARAMS_CATEGORY = {
#     "headers": {
#         'method': 'GET',
#         'scheme': 'https',
#         'path': '/v4/venues/63443c821dd17f940c4360fa/menu/data?show_subcategories=true&show_weighted_items=true&show_fulfillment_lead_times=false&unit_prices=true',
#         'authority': 'restaurant-api.wolt.com',
#         'accept': '*/*',
#         'clientversionnumber': '242102',
#         'app-locale': 'ru-KZ',
#         'app-currency-format': 'McKgMjM0LDU2wqDCpA==',
#         'app-language': 'ru',
#         'client-version': '24.21.2',
#         'accept-language': 'ru-KZ;q=1.00,kk-KZ;q=0.50',
#         # 'accept-encoding': 'gzip, deflate, br',
#         'x-wolt-visitor-id': 'EBE02D7C-B413-4B82-ACBB-6914041201A3',
#         'w-wolt-session-id': 'EF78E654-AF44-4B4A-B1C1-41774DAF6D6A',
#         'platform': 'iPhone',
#         'user-agent': 'Wolt/242102; Build/8854; iOS/17.4.1; iPhone; ru',
#         'userlocationlng': '76.925551',
#         'userlocationlat': '43.234786',
#         'Host': 'restaurant-api.wolt.com',
#         # 'Connection': 'close'


#      },

#     "params": {
#         'show_subcategories': 'true',
#         'show_weighted_items': 'true',
#         'show_fulfillment_lead_times': 'false',
#         'unit_prices': 'true',
        
#     },

#     "method": "GET",
#     "body": ""
# }
