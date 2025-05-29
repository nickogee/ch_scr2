
############################### Получение токена
URL_TOKEN = 'https://lavka.yandex.kz/'
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
    'user-agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    
  },
  "body": None,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}


############################### Основной запрос к каталогу
URL_CATALOG = 'https://lavka.yandex.kz/api/v1/providers/v2/category'

EMPTY_SK = r'{}'

# LAST_ADDRESS_MASK = r'{%22latitude%22:43.217141%2C%22longitude%22:76.881999}'
LAT_MASK = '@LAT_MASK@'
LONG_MASK = '@LONG_MASK@'
# LAST_ADDRESS_MASK = r'{%22latitude%22:@LAT_MASK@%2C%22longitude%22:@LONG_MASK@}'
# LAST_VISIT_TIME_MASK = '@CVISIT_TIME_MASK@'
# COOKIE = f'is_gdpr=0; yashr=4194119911734330262; receive-cookie-deprecation=1; is_gdpr_b=CPeCThCxpAIoAg==; _ym_uid=1734330265882058229; _ym_d=1734330266; yandexuid=2536956921734328816; yuidss=2536956921734328816; i=U+pCoiyXZchSVoWro9oRASjf9xgsd9doI5Bb0XVKTtbesp55CiWBHnL9puj0nCYoUYaHXXHDwYWHDgIO5fabiBqkEY4=; yp=1734416666.yu.1765851031734330262; lavka__viewed_banners={EMPTY_SK}; lavka__confirmed_restriction=null; lavka__modal_viewes={EMPTY_SK}; lavka__sku_scroll_down_button_shown_times=0; lavka__tags_applied_from_product_card_times=0; lavka__selected_subcategory_group_by_category={EMPTY_SK}; lavka__permanently_closed_floating_buttons={EMPTY_SK}; lavka__install_app_modal_shown_at=0; lavka__install_app_bottom_sheet_shown_at=0; lavka__last_timezone=Asia/Almaty; lavka__session_counter=1; lavka__userpreflang=ru; lavka__adult_confirmed=false; ymex=1736922266.oyu.1765851031734330262#2049710394.yrts.1734350394; bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTMxIiwgIkNocm9taXVtIjt2PSIxMzEiLCAiTm90X0EgQnJhbmQiO3Y9IjI0IhoFImFybSIiECIxMzEuMC42Nzc4LjE0MCIqAj8wMgIiIjoHIm1hY09TIkIIIjE0LjUuMCJKBCI2NCJSXCJHb29nbGUgQ2hyb21lIjt2PSIxMzEuMC42Nzc4LjE0MCIsIkNocm9taXVtIjt2PSIxMzEuMC42Nzc4LjE0MCIsIk5vdF9BIEJyYW5kIjt2PSIyNC4wLjAuMCIiWgI/MGChx5O8Bg==; lavka__session=60128599-6f7b-4e42-93de-ea2efb8bb87b; lavka__lastdetreg=KZ; lavka__lastdetlang=ru; lavka__out_of_edition_limit_orders=[]; lavka__last_address={LAST_ADDRESS_MASK}; gdpr=0; lavka__authProxyState=authorized%3Ad3ecd21dfbd94f7c857b68b886bbacc4%3A-1646493438%3Afalse; lavka__auth-proxy-ct=xNpzfNP2cvu5IvaLQoJFC1oHaL8%3D%3A1734350389; _yasc=rhyG+g74WaF6YKF4JO08W6zWwhsnbGVDuzX0tN0fR6OuYiIyLgNHE1G+8C9R/UJ03SxCs2pyqA==; lavka_referral_award_informer_views=23; lavka_referral_informer_views=23; lavka__last_visit_time={LAST_VISIT_TIME_MASK}',

CURRENT_CATEGORY_MASK = '@CAT_MASK@'
CURRENT_CATEGORY_ID_MASK = '@CAT_ID_MASK@'
LAYOUT_ID_MASK = '@LAYOUT_ID_MASK@'
CONTENT_LENGHT_MASK = '@CONT_LEGHT_MASK@'
PARAMS_CATALOG = {
    "headers": {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': None,
        'Content-Type': 'application/json',
        # 'Cookie': None,
        'Host': 'lavka.yandex.kz',
        'Origin': 'https://lavka.yandex.kz',
        'Referer': f'https://lavka.yandex.kz/category/{CURRENT_CATEGORY_MASK}',
        'Sec-Ch-Ua': r'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "macOS",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Captcha-Language': 'ru',
        'X-Captcha-Service': 'lavka',
        'X-Csrf-Token': None,
        'X-Lavka-Web-City': 162,
        'X-Lavka-Web-Locale': 'ru-KZ',
        'X-Requested-With': 'XMLHttpRequest' 
        },

    "method": "POST",
    "body": r'{"modes":["grocery"],"categoryId":"@CAT_MASK@","categoryPath":{"groupId":"@CAT_ID_MASK@","layoutId":"@LAYOUT_ID_MASK@"},"position":{"location":[@LONG_MASK@,@LAT_MASK@]},"additionalData":{},"categoryCarouselsEnabled":true,"currencySign":"₸","depotType":"regular"}'
        }

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
