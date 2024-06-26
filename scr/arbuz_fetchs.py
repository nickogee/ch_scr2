
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

URL_FST = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?&limit=40&token="
URL_NXT = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?page={PAGE}&limit=40&token="

# -------------- изменяемое -- начало------
PARAMS =  {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-locale": "ru",
    "cookie": "_ym_uid=1684821805258414270; _ym_d=1684821805; __stripe_mid=d9479f81-e1ab-429e-bd1d-7a5f769afc318461b1; arbuz-kz_jwt_v3=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNGNlOGY4NS0xYTZiLTQ2NWEtYTExMi0xY2VkZTg3NDYzZDEiLCJpc3MiOiJZSDhzWmdQOExTUGR4eFhsUFZoRWdoOE5UdXc2SlJLZCIsImlhdCI6MTY4NDgyODkwNSwiZXhwIjo0ODM4NDI4OTA1LCJjb25zdW1lciI6eyJpZCI6ImU1YzRlYTA1LWY4ZTgtNDJiZC1iMDJhLWNmMzNlODAyZjA5NiIsIm5hbWUiOiJhcmJ1ei1rei53ZWIuZGVza3RvcCJ9LCJjaWQiOm51bGx9.LiA23DwWoe2U3UqcTymHm5HmkrHsOodhlwOG0oMheHM; PHPSESSID=2d40997f17ed47991444869356705cfc; mindboxDeviceUUID=b5252e82-08f4-40d7-8fdf-75bf7b4ea57a; directCrm-session=%7B%22deviceGuid%22%3A%22b5252e82-08f4-40d7-8fdf-75bf7b4ea57a%22%7D; _gcl_au=1.1.1664444597.1698898538; _gid=GA1.2.90459052.1698898538; _fbp=fb.1.1698898538747.1873771590; _ym_isad=2; _tt_enable_cookie=1; _ttp=kDUI5tzmSOmtcnN0AZ2Tmg6J4Sx; _ga=GA1.2.688556888.1698898538; _ga_0X26SLE0CQ=GS1.1.1698906573.2.0.1698906573.60.0.0",
    "Referer": "https://arbuz.kz/ru/almaty/catalog/cat/225164-svezhie_ovoshi_i_frukty",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": None,
  "method": "GET"
}
# -------------- изменяемое -- конец------
###############
