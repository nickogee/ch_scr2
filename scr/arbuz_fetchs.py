
PAGE = '@PAGE@'
SUB_CATALOG = '@SUBCATALOG@'
LOUNCH_LIMIT = 3
CITY = '@CITY@'
HREF = '@HREF@'

CATEGORIES_ABZ = [
    {'title': 'Фрукты', 'href': f"/ru/{CITY}/catalog/cat/225177-frukty", 'catalog': '225177'},
    {'title': 'Овощи', 'href': f"/ru/{CITY}/catalog/cat/225178-ovoshi", 'catalog': '225178'},
    {'title': 'Зелень', 'href': f"/ru/{CITY}/catalog/cat/225176-zelen", 'catalog': '225176'},
    {'title': 'Арбузы и дыни', 'href': f"/ru/{CITY}/catalog/cat/225569-arbuzy_i_dyni", 'catalog': '225569'},
    {'title': 'Ягоды', 'href': f"/ru/{CITY}/catalog/cat/225562-yagody", 'catalog': '225562'},
    {'title': 'Грибы', 'href': f"/ru/{CITY}/catalog/cat/225444-griby", 'catalog': '225444'},
    {'title': 'Соленья', 'href': f"/ru/{CITY}/catalog/cat/225445-solenya", 'catalog': '225445'},
    {'title': 'Сухофрукты Arbuz Select', 'href': f"/ru/{CITY}/collections/249886-suhofrukty_arbuz_select", 'catalog': '249886'},
    {'title': 'Фрукты и овощи замороженные', 'href': f"/ru/{CITY}/catalog/cat/225189-frukty_i_ovoshi_zamorozhennye", 'catalog': '225189'},
    {'title': 'Молоко, сливки', 'href': f"/ru/{CITY}/catalog/cat/19986-moloko_slivki", 'catalog': '19986'},
    {'title': 'Сыр', 'href': f"/ru/{CITY}/catalog/cat/20160-syr", 'catalog': '20160'},
    {'title': 'Кефир, творог, сметана', 'href': f"/ru/{CITY}/catalog/cat/225446-kefir_tvorog_smetana", 'catalog': '225446'},
    {'title': 'Яйца, масло, маргарин', 'href': f"/ru/{CITY}/catalog/cat/225245-yaica_maslo_margarin", 'catalog': '225245'},
    {'title': 'Йогурты, сырки, десерты', 'href': f"/ru/{CITY}/catalog/cat/225171-iogurty_syrki_deserty", 'catalog': '225171'},
    {'title': 'Мясо и стейки', 'href': f"/ru/{CITY}/catalog/cat/19907-myaso_i_steiki", 'catalog': '19907'},
    {'title': 'Курица, индейка и птица', 'href': f"/ru/{CITY}/catalog/cat/225173-kurica_indeika_i_ptica", 'catalog': '225173'},
    {'title': 'Рыба', 'href': f"/ru/{CITY}/catalog/cat/225175-ryba", 'catalog': '225175'},
    {'title': 'Морепродукты', 'href': f"/ru/{CITY}/catalog/cat/225174-moreprodukty", 'catalog': '225174'},
    {'title': 'Фарш', 'href': f"/ru/{CITY}/catalog/cat/225599-farsh", 'catalog': '225599'},
    {'title': 'Полуфабрикаты и маринады', 'href': f"/ru/{CITY}/catalog/cat/225609-polufabrikaty_i_marinady", 'catalog': '225609'},
    {'title': 'Молоко, сыр', 'href': f"/ru/{CITY}/catalog/cat/225269-moloko_syr", 'catalog': '225269'},
    {'title': 'Мясо, птица', 'href': f"/ru/{CITY}/catalog/cat/225286-myaso_ptica", 'catalog': '225286'},
    {'title': 'Бакалея', 'href': f"/ru/{CITY}/catalog/cat/225287-bakaleya", 'catalog': '225287'},
    {'title': 'Деликатесы', 'href': f"/ru/{CITY}/catalog/cat/225488-delikatesy", 'catalog': '225488'},
    {'title': 'Сыры Arbuz Select', 'href': f"/ru/{CITY}/collections/250017-syry_arbuz_select", 'catalog': '250017'},
    {'title': 'Хлеб и хлебцы', 'href': f"/ru/{CITY}/catalog/cat/20118-hleb_i_hlebcy", 'catalog': '20118'},
    {'title': 'Выпечка', 'href': f"/ru/{CITY}/catalog/cat/225179-vypechka", 'catalog': '225179'},
    {'title': 'Лаваш, пита, лепешки', 'href': f"/ru/{CITY}/catalog/cat/225452-lavash_pita_lepeshki", 'catalog': '225452'},
    {'title': 'Колбасы', 'href': f"/ru/{CITY}/catalog/cat/19855-kolbasy", 'catalog': '19855'},
    {'title': 'Сосиски, сардельки', 'href': f"/ru/{CITY}/catalog/cat/225180-sosiski_sardelki", 'catalog': '225180'},
    {'title': 'Мясные деликатесы', 'href': f"/ru/{CITY}/catalog/cat/225451-myasnye_delikatesy", 'catalog': '225451'},
    {'title': 'Завтраки', 'href': f"/ru/{CITY}/catalog/cat/225576-zavtraki", 'catalog': '225576'},
    {'title': 'Вторые блюда', 'href': f"/ru/{CITY}/catalog/cat/225201-vtorye_blyuda", 'catalog': '225201'},
    {'title': 'Салаты, супы', 'href': f"/ru/{CITY}/catalog/cat/225572-salaty_supy", 'catalog': '225572'},
    {'title': 'Сэндвичи и круассаны', 'href': f"/ru/{CITY}/catalog/cat/225577-sendvichi_i_kruassany", 'catalog': '225577'},
    {'title': 'ПП-обеды', 'href': f"/ru/{CITY}/catalog/cat/225289-pp-obedy", 'catalog': '225289'},
    {'title': 'Детские обеды', 'href': f"/ru/{CITY}/catalog/cat/225300-detskie_obedy", 'catalog': '225300'},
    {'title': 'Десерты', 'href': f"/ru/{CITY}/catalog/cat/225303-deserty", 'catalog': '225303'},
    {'title': 'Торты и пирожные', 'href': f"/ru/{CITY}/catalog/cat/225607-torty_i_pirozhnye", 'catalog': '225607'},
    {'title': 'Орехи и сухофрукты', 'href': f"/ru/{CITY}/catalog/cat/225304-orehi_i_suhofrukty", 'catalog': '225304'},
    {'title': 'Чипсы', 'href': f"/ru/{CITY}/catalog/cat/225604-chipsy", 'catalog': '225604'},
    {'title': 'Сухарики и снеки', 'href': f"/ru/{CITY}/catalog/cat/225605-suhariki_i_sneki", 'catalog': '225605'},
    {'title': 'Варенье, джемы, сиропы', 'href': f"/ru/{CITY}/catalog/cat/225248-varene_dzhemy_siropy", 'catalog': '225248'},
    {'title': 'Конфеты', 'href': f"/ru/{CITY}/catalog/cat/225041-konfety", 'catalog': '225041'},
    {'title': 'Мёд', 'href': f"/ru/{CITY}/catalog/cat/224601-m_d", 'catalog': '224601'},
    {'title': 'Печенье, вафли, пряники', 'href': f"/ru/{CITY}/catalog/cat/225042-pechene_vafli_pryaniki", 'catalog': '225042'},
    {'title': 'Шоколад, батончики, паста', 'href': f"/ru/{CITY}/catalog/cat/225247-shokolad_batonchiki_pasta", 'catalog': '225247'},
    {'title': 'Крупы, бобовые', 'href': f"/ru/{CITY}/catalog/cat/224398-krupy_bobovye", 'catalog': '224398'},
    {'title': 'Консервы', 'href': f"/ru/{CITY}/catalog/cat/20205-konservy", 'catalog': '20205'},
    {'title': 'Макароны и лапша', 'href': f"/ru/{CITY}/catalog/cat/224399-makarony_i_lapsha", 'catalog': '224399'},
    {'title': 'Майонез, кетчуп, горчица', 'href': f"/ru/{CITY}/catalog/cat/224588-maionez_ketchup_gorchica", 'catalog': '224588'},
    {'title': 'Масло растительное', 'href': f"/ru/{CITY}/catalog/cat/225448-maslo_rastitelnoe", 'catalog': '225448'},
    {'title': 'Соусы и уксусы', 'href': f"/ru/{CITY}/catalog/cat/225450-sousy_i_uksusy", 'catalog': '225450'},
    {'title': 'Продукты быстрого приготовления', 'href': f"/ru/{CITY}/catalog/cat/25400-produkty_bystrogo_prigotovleniya", 'catalog': '25400'},
    {'title': 'Сухие завтраки', 'href': f"/ru/{CITY}/catalog/cat/224533-suhie_zavtraki", 'catalog': '224533'},
    {'title': 'Сахар, соль, специи', 'href': f"/ru/{CITY}/catalog/cat/224402-sahar_sol_specii", 'catalog': '224402'},
    {'title': 'Мука', 'href': f"/ru/{CITY}/catalog/cat/225449-muka", 'catalog': '225449'},
    {'title': 'Для выпечки', 'href': f"/ru/{CITY}/catalog/cat/225181-dlya_vypechk", 'catalog': '225181'},
    {'title': 'Котлеты, тефтели, наггетсы', 'href': f"/ru/{CITY}/catalog/cat/225185-kotlety_tefteli_naggetsy", 'catalog': '225185'},
    {'title': 'Пельмени, вареники, манты', 'href': f"/ru/{CITY}/catalog/cat/225184-pelmeni_vareniki_manty", 'catalog': '225184'},
    {'title': 'Хлеб и выпечка', 'href': f"/ru/{CITY}/catalog/cat/225186-hleb_i_vypechka", 'catalog': '225186'},
    {'title': 'Мороженое', 'href': f"/ru/{CITY}/catalog/cat/225209-morozhenoe", 'catalog': '225209'},
    {'title': 'Пицца и пироги', 'href': f"/ru/{CITY}/catalog/cat/225188-picca_i_pirogi", 'catalog': '225188'},
    {'title': 'Самса, пирожки, чебуреки', 'href': f"/ru/{CITY}/catalog/cat/225187-samsa_pirozhki_chebureki", 'catalog': '225187'},
    {'title': 'Тесто и основа для пиццы', 'href': f"/ru/{CITY}/catalog/cat/225252-testo_i_osnova_dlya_piccy", 'catalog': '225252'},
    {'title': 'Вода', 'href': f"/ru/{CITY}/catalog/cat/20697-voda", 'catalog': '20697'},
    {'title': 'Газированные напитки и энергитики', 'href': f"/ru/{CITY}/catalog/cat/20784-gazirovannye_napitki_i_energitiki", 'catalog': '20784'},
    {'title': 'Соки и морсы', 'href': f"/ru/{CITY}/catalog/cat/20739-soki_i_morsy", 'catalog': '20739'},
    {'title': 'Кофе и какао', 'href': f"/ru/{CITY}/catalog/cat/225172-kofe_i_kakao", 'catalog': '225172'},
    {'title': 'Чай', 'href': f"/ru/{CITY}/catalog/cat/225447-cha", 'catalog': '225447'},
    {'title': 'Любимые напитки', 'href': f"/ru/{CITY}/collections/250562-lyubimye_napitki#/", 'catalog': '250562'},
    {'title': 'Средства для мытья посуды', 'href': f"/ru/{CITY}/catalog/cat/224494-sredstva_dlya_mytya_posudy", 'catalog': '224494'},
    {'title': 'Стирка и уход за бельём', 'href': f"/ru/{CITY}/catalog/cat/224405-stirka_i_uhod_za_bel_m", 'catalog': '224405'},
    {'title': 'Для уборки', 'href': f"/ru/{CITY}/catalog/cat/225190-dlya_uborki", 'catalog': '225190'},
    {'title': 'Всё для дома', 'href': f"/ru/{CITY}/catalog/cat/225211-vs_dlya_doma", 'catalog': '225211'},
    {'title': 'Дача, сад и огород', 'href': f"/ru/{CITY}/catalog/cat/225370-dacha_sad_i_ogorod", 'catalog': '225370'},
    {'title': 'Для декора', 'href': f"/ru/{CITY}/catalog/cat/225502-dlya_dekora", 'catalog': '225502'},
    {'title': 'Детское питание и смеси', 'href': f"/ru/{CITY}/catalog/cat/224478-detskoe_pitanie_i_smesi", 'catalog': '224478'},
    {'title': 'Аксессуары для кормления', 'href': f"/ru/{CITY}/catalog/cat/224624-aksessuary_dlya_kormleniya", 'catalog': '224624'},
    {'title': 'Подгузники и гигиена', 'href': f"/ru/{CITY}/catalog/cat/25414-podguzniki_i_gigiena", 'catalog': '25414'},
    {'title': 'Для школы', 'href': f"/ru/{CITY}/catalog/cat/21969-dlya_shkoly", 'catalog': '21969'},
    {'title': 'Игрушки', 'href': f"/ru/{CITY}/catalog/cat/224620-igrushki", 'catalog': '224620'},
    {'title': 'Женские гигиенические средства', 'href': f"/ru/{CITY}/catalog/cat/224492-zhenskie_gigienicheskie_sredstva", 'catalog': '224492'},
    {'title': 'Макияж', 'href': f"/ru/{CITY}/catalog/cat/225251-makiyazh", 'catalog': '225251'},
    {'title': 'Туалетная бумага и салфетки', 'href': f"/ru/{CITY}/catalog/cat/224493-tualetnaya_bumaga_i_salfetki", 'catalog': '224493'},
    {'title': 'Уход за волосами', 'href': f"/ru/{CITY}/catalog/cat/224409-uhod_za_volosami", 'catalog': '224409'},
    {'title': 'Уход за лицом', 'href': f"/ru/{CITY}/catalog/cat/224583-uhod_za_licom", 'catalog': '224583'},
    {'title': 'Уход за полостью рта', 'href': f"/ru/{CITY}/catalog/cat/224413-uhod_za_polostyu_rta", 'catalog': '224413'},
    {'title': 'Уход за телом', 'href': f"/ru/{CITY}/catalog/cat/21687-uhod_za_telom", 'catalog': '21687'},
    {'title': 'Антисептик, мази', 'href': f"/ru/{CITY}/catalog/cat/224425-antiseptik_mazi", 'catalog': '224425'},
    {'title': 'Витамины, витаминные комплексы', 'href': f"/ru/{CITY}/catalog/cat/225071-vitaminy_vitaminnye_kompleksy", 'catalog': '225071'},
    {'title': 'Все для спорта', 'href': f"/ru/{CITY}/catalog/cat/225254-vse_dlya_sporta", 'catalog': '225254'},
    {'title': 'Товары для взрослых', 'href': f"/ru/{CITY}/catalog/cat/225310-tovary_dlya_vzroslyh", 'catalog': '225310'},
    {'title': 'Травы, чаи, настойки', 'href': f"/ru/{CITY}/catalog/cat/225149-travy_chai_nastoiki", 'catalog': '225149'},
    {'title': 'Подарки, товары для праздников', 'href': f"/ru/{CITY}/catalog/cat/225432-podarki_tovary_dlya_prazdnikov", 'catalog': '225432'},
    {'title': 'Соевые продукты', 'href': f"/ru/{CITY}/catalog/cat/224575-soevye_produkty", 'catalog': '224575'},
    {'title': 'Ветаптека', 'href': f"/ru/{CITY}/catalog/cat/225373-vetapteka", 'catalog': '225373'},
    {'title': 'Гигиена и уход за животными', 'href': f"/ru/{CITY}/catalog/cat/202652-gigiena_i_uhod_za_zhivotnymi", 'catalog': '202652'},
    {'title': 'Для собак', 'href': f"/ru/{CITY}/catalog/cat/202170-dlya_sobak", 'catalog': '202170'},
    {'title': 'Для кошек', 'href': f"/ru/{CITY}/catalog/cat/225036-dlya_koshek", 'catalog': '225036'},
    {'title': 'Для грызунов', 'href': f"/ru/{CITY}/catalog/cat/225411-dlya_gryzunov", 'catalog': '225411'},
    {'title': 'Для птиц', 'href': f"/ru/{CITY}/catalog/cat/225282-dlya_ptic", 'catalog': '225282'},
    {'title': 'Для рыб', 'href': f"/ru/{CITY}/catalog/cat/225493-dlya_ryb", 'catalog': '225493'},
    {'title': 'Азиатская кухня', 'href': f"/ru/{CITY}/catalog/cat/167005-aziatskaya_kuhnya", 'catalog': '167005'},
] 

FAST_CATEGORIES_ABZ = [
    {'title': 'Фрукты', 'href': f"/ru/{CITY}/catalog/cat/225177-frukty", 'catalog': '225177'},
    {'title': 'Овощи', 'href': f"/ru/{CITY}/catalog/cat/225178-ovoshi", 'catalog': '225178'},
    {'title': 'Зелень', 'href': f"/ru/{CITY}/catalog/cat/225176-zelen", 'catalog': '225176'},
    {'title': 'Арбузы и дыни', 'href': f"/ru/{CITY}/catalog/cat/225569-arbuzy_i_dyni", 'catalog': '225569'},
    {'title': 'Ягоды', 'href': f"/ru/{CITY}/catalog/cat/225562-yagody", 'catalog': '225562'},
    {'title': 'Грибы', 'href': f"/ru/{CITY}/catalog/cat/225444-griby", 'catalog': '225444'},
    {'title': 'Соленья', 'href': f"/ru/{CITY}/catalog/cat/225445-solenya", 'catalog': '225445'},
    {'title': 'Сухофрукты Arbuz Select', 'href': f"/ru/{CITY}/collections/249886-suhofrukty_arbuz_select", 'catalog': '249886'},
    {'title': 'Фрукты и овощи замороженные', 'href': f"/ru/{CITY}/catalog/cat/225189-frukty_i_ovoshi_zamorozhennye", 'catalog': '225189'},
]

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
    "Referer": f"https://arbuz.kz/ru/{HREF}",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": None,
  "method": "GET"
}
# -------------- изменяемое -- конец------
###############
