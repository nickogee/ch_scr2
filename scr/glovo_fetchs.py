
# CATEGORIES_GLV = [
#     {'title': "Фрукты и Овощи", 'slug': "frukty-i-ovoshchi-sc.261845244"},
#     {'title': "Готовая Еда", 'slug': "gotovaya-eda-sc.261845245"},
#     {'title': "Молочные Продукты", 'slug': "molochnye-produkty-sc.261845246"},
#     {'title': "Деликатесы", 'slug': "delikatesy-sc.261845247"},
#     {'title': "Хлеб и Выпечка", 'slug': "hleb-i-vypechka-sc.261845248"}, 
#     {'title': "Кофе, Сахар", 'slug': "kofe-sahar-sc.261845249"},
#     {'title': "Бакалея", 'slug': "bakaleya-sc.261845250"},
#     {'title': "Сладости и Десерты", 'slug': "sladosti-i-deserty-sc.261845251"}, 
#     {'title': "Снеки", 'slug': "sneki-sc.261845252"}, 
#     {'title': "Мороженое и Заморозка", 'slug': "morozhenoe-i-zamorozka-sc.261845253"},
#     {'title': "Холодные Напитки", 'slug': "holodnye-napitki-sc.261845254"},
#     {'title': "Соки, Энергетики и Вода", 'slug': "soki-energetiki-i-voda-sc.261845255"},
#     {'title': "Аптека", 'slug': "apteka-sc.261845256"},
#     {'title': "Товары для детей", 'slug': "tovary-dlya-detey-sc.261845257"},
#     {'title': "Личная Гигиена и Красота", 'slug': "lichnaya-gigiena-i-krasota-sc.261845258"},
#     {'title': "Бытовая Химия", 'slug': "bytovaya-himiya-sc.261845259"},
#     {'title': "Товары для животных", 'slug': "tovary-dlya-zhivotnyh-sc.261845260"},
#     {'title': "Товары для дома", 'slug': "tovary-dlya-doma-sc.261845261"},
# ]


CATEGORIES_GLV = [
    {'title': "Фрукты и Овощи", 'slug': "frukty-i-ovoshchi-sc.295590"},
    {'title': "Снова в школу", 'slug': "snova-v-shkolu-sc.14277937"},
    {'title': "Готовая еда", 'slug': "gotovaya-eda-sc.295596"},
    {'title': "Молочные Продукты", 'slug': "molochnye-produkty-sc.295605"},
    {'title': "Сыры и Мясные закуски", 'slug': "syry-i-myasnye-zakuski-sc.295815"},
    {'title': "Хлеб и Выпечка", 'slug': "hleb-i-vypechka-sc.295574"},
    {'title': "Сладости и Десерты", 'slug': "sladosti-i-deserty-sc.295653"},
    {'title': "Снеки", 'slug': "sneki-sc.295654"},
    {'title': "Мороженое и Заморозка", 'slug': "morozhenoe-i-zamorozka-sc.295687"},
    {'title': "Мясо, Птица и Рыба", 'slug': "myaso-ptitsa-i-ryba-sc.6288316"},
    {'title': "Энергетические напитки", 'slug': "energeticheskie-napitki-sc.14277922"},
    {'title': "Напитки", 'slug': "napitki-sc.14277927"},
    {'title': "Бакалея", 'slug': "bakaleya-sc.295821"},
    {'title': "Алкоголь", 'slug': "alkogol-sc.851917"},
    {'title': "Табачная продукция", 'slug': "tabachnaya-produktsiya-sc.1911184"},
    {'title': "Чай, кофе и какао", 'slug': "chay-kofe-i-kakao-sc.295818"},
    {'title': "Аптека", 'slug': "apteka-sc.801380"},
    {'title': "Личная Гигиена и Красота", 'slug': "lichnaya-gigiena-i-krasota-sc.295938"},
    {'title': "Бытовая Химия", 'slug': "bytovaya-himiya-sc.295994"},
    {'title': "Детские товары", 'slug': "detskie-tovary-sc.295902"},
    {'title': "Товары для домашних животных", 'slug': "tovary-dlya-domashnih-zhivotnyh-sc.296065"},
    {'title': "Товары для Дома", 'slug': "tovary-dlya-doma-sc.296130"},
]

PARAMS =  {
  "headers": {
    "accept": "application/json",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "glovo-api-version": "14",
    "glovo-app-development-state": "Production",
    "glovo-app-platform": "web",
    "glovo-app-type": "customer",
    "glovo-app-version": "7",
    "glovo-delivery-location-accuracy": "0",
    "glovo-delivery-location-latitude": "43.2223033",
    "glovo-delivery-location-longitude": "76.8514204",
    "glovo-delivery-location-timestamp": "1685445097692",
    "glovo-device-id": "1376212903",
    "glovo-dynamic-session-id": "9e3c2d30-ba27-436a-8236-14dd7439c897",
    "glovo-language-code": "ru",
    "glovo-location-city-code": "ALA",
    "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
  },
  "referrerPolicy": "same-origin",
  "body": None,
  "method": "GET"
}

URL_SERV = "https://api.glovoapp.com/v3/"
SLUG = '@SLUG@'
URL_FST = f"https://api.glovoapp.com/v3/stores/325275/addresses/548633/content?nodeType=DEEP_LINK&link={SLUG}"

# Фрукты Овощи:
# URL_FST = "https://api.glovoapp.com/v3/stores/309810/addresses/548633/content?nodeType=DEEP_LINK&link=frukty-i-ovoshchi-sc.260612711"
###############

