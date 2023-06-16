
CATEGORIES_ABZ = [
    {'title': 'Свежие овощи и фрукты', 'href': "/ru/almaty/catalog/cat/225164-svezhie_ovoshi_i_frukty", 'catalog': '225164'},
    {'title': 'Напитки', 'href': "/ru/almaty/catalog/cat/14-napitki", 'catalog': '14'},
    {'title': 'Молоко, сыр, масло, яйцаx', 'href': "/ru/almaty/catalog/cat/225161-moloko_syr_maslo_yaica", 'catalog': '225161'},
    {'title': 'Рыба и морепродукты', 'href': "/ru/almaty/catalog/cat/225163-ryba_i_moreprodukty", 'catalog': '225163'},
    {'title': 'Кулинария', 'href': "/ru/almaty/catalog/cat/225253-kulinariya", 'catalog': '225253'},
    {'title': 'Фермерская лавка', 'href': "/ru/almaty/catalog/cat/225268-fermerskaya_lavka", 'catalog': '225268'},
    {'title': 'Мясо, птица', 'href': "/ru/almaty/catalog/cat/225162-myaso_ptica", 'catalog': '225162'},
    {'title': 'Хлеб, выпечка', 'href': "/ru/almaty/catalog/cat/225165-hleb_vypechka", 'catalog': '225165'},
    {'title': 'Колбасы', 'href': "/ru/almaty/catalog/cat/225167-kolbasy", 'catalog': '225167'},
    {'title': 'Замороженные продукты', 'href': "/ru/almaty/catalog/cat/225183-zamorozhennye_produkty", 'catalog': '225183'},
    {'title': 'Растительные продукты', 'href': "/ru/almaty/catalog/cat/225244-rastitelnye_produkty", 'catalog': '225244'},
    {'title': 'Все для готовки и выпечки', 'href': "/ru/almaty/catalog/cat/225168-vse_dlya_gotovki_i_vypechki", 'catalog': '225168'},
    {'title': 'Сладости', 'href': "/ru/almaty/catalog/cat/225166-sladosti", 'catalog': '225166'},
    {'title': 'Крупы, консервы, снэки', 'href': "/ru/almaty/catalog/cat/225169-krupy_konservy_sneki", 'catalog': '225169'},
    {'title': 'Детям', 'href': "/ru/almaty/catalog/cat/19-detyam", 'catalog': '19'},
    {'title': 'Кухни народов мира', 'href': "/ru/almaty/catalog/cat/225170-kuhni_narodov_mira", 'catalog': '225170'},
    {'title': 'Всё для дома', 'href': "/ru/almaty/catalog/cat/16-vs_dlya_doma", 'catalog': '16'},
    {'title': 'Здоровье', 'href': "/ru/almaty/catalog/cat/225075-zdorove", 'catalog': '225075'},
    {'title': 'Красота', 'href': "/ru/almaty/catalog/cat/224407-krasota", 'catalog': '224407'},
    {'title': 'Zoo Магазин', 'href': "/ru/almaty/catalog/cat/20-zoo_magazin", 'catalog': '20'},
    {'title': 'К празднику', 'href': "/ru/almaty/catalog/cat/225063-k_prazdniku", 'catalog': '225063'},
] 

PAGE = '@PAGE@'
SUB_CATALOG = '@SUBCATALOG@'
URL_FST = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?&limit=32"
URL_NXT = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?page={PAGE}&limit=32"

# -------------- изменяемое -- начало------
PARAMS =  {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-locale": "ru",
    "cookie": "PHPSESSID=9a8f446906c013e17120771dfa400006; mindboxDeviceUUID=b5252e82-08f4-40d7-8fdf-75bf7b4ea57a; directCrm-session=%7B%22deviceGuid%22%3A%22b5252e82-08f4-40d7-8fdf-75bf7b4ea57a%22%7D; _gcl_au=1.1.1678211147.1684821804; _tt_enable_cookie=1; _ttp=iaamILCQSEGPYS4DtIWnhO6FfSw; _fbp=fb.1.1684821805080.196734901; _ym_uid=1684821805258414270; _ym_d=1684821805; __stripe_mid=d9479f81-e1ab-429e-bd1d-7a5f769afc318461b1; arbuz-kz_jwt_v3=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNGNlOGY4NS0xYTZiLTQ2NWEtYTExMi0xY2VkZTg3NDYzZDEiLCJpc3MiOiJZSDhzWmdQOExTUGR4eFhsUFZoRWdoOE5UdXc2SlJLZCIsImlhdCI6MTY4NDgyODkwNSwiZXhwIjo0ODM4NDI4OTA1LCJjb25zdW1lciI6eyJpZCI6ImU1YzRlYTA1LWY4ZTgtNDJiZC1iMDJhLWNmMzNlODAyZjA5NiIsIm5hbWUiOiJhcmJ1ei1rei53ZWIuZGVza3RvcCJ9LCJjaWQiOm51bGx9.LiA23DwWoe2U3UqcTymHm5HmkrHsOodhlwOG0oMheHM; _gcl_aw=GCL.1686913790.CjwKCAjwkLCkBhA9EiwAka9QRp-vZZjIR_fHXg8FbzzWhRLwjYR7WYEJcG6V3Dh7dXAJ30VoUGNXaBoCWkkQAvD_BwE; _gid=GA1.2.434534080.1686913790; _gac_UA-109863448-1=1.1686913790.CjwKCAjwkLCkBhA9EiwAka9QRp-vZZjIR_fHXg8FbzzWhRLwjYR7WYEJcG6V3Dh7dXAJ30VoUGNXaBoCWkkQAvD_BwE; _ym_visorc=w; _ym_isad=2; __stripe_sid=f664f4fc-a4a9-4c98-a9ee-8a1011469c43a053c9; _dc_gtm_UA-109863448-1=1; _ga=GA1.2.327912292.1684821804; _ga_0X26SLE0CQ=GS1.1.1686913789.9.1.1686914073.33.0.0",
    "Referer": "https://arbuz.kz/ru/almaty/catalog/cat/14-napitki",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": None,
  "method": "GET"
}

# CATALOG_NUMBER = 225162
# CATALOG_NUMBER = 225164 # Фрукты Овощи
# -------------- изменяемое -- конец------
###############
