
PAGE = '@PAGE@'
SUB_CATALOG = '@SUBCATALOG@'
LOUNCH_LIMIT = 5
CITY = '@CITY@'
HREF = '@HREF@'

'''
Промт для вытаскивания категорий из html страницы, вытаскиваем title и href (html скопирован с сайта arbuz.kz)
<div data-v-6857b387="" class="submenu"><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225178-ovoshi" class="submenu-item">
          Овощи
        </a><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225176-zelen" class="submenu-item">
          Зелень
        </a><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225444-griby" class="submenu-item">
          Грибы
        </a><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225177-frukty" class="submenu-item">
          Фрукты
        </a><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225562-yagody" class="submenu-item">
          Ягоды
        </a><a data-v-6857b387="" href="/ru/almaty/catalog/cat/225445-solenya" class="submenu-item">
          Соленья
        </a></div>


#1 Read the file "scr/cat" and get tags "<a></a>" excluding the first tag "<a></a>" into tags "<div></div>".
#2 extract from tags "<a></a>" from #1 text end the "href" feature.
#3  make a structure like a var "CATEGORIES_ABZ" in "arbuz_fetch.py" where 'titele': text from #2, 'href': href from #2, 'catalog': a part of string in href from #2.
#4 write result from #3 into new var "CATEGORIES_ABZ_NEW" in "arbuz_fetch.py"
'''

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

CATEGORIES_ABZ = [
    {'title': 'Зелень', 'href': f"/ru/{CITY}/catalog/cat/225176-zelen", 'catalog': '225176'},
    {'title': 'Грибы', 'href': f"/ru/{CITY}/catalog/cat/225444-griby", 'catalog': '225444'},
    {'title': 'Фрукты', 'href': f"/ru/{CITY}/catalog/cat/225177-frukty", 'catalog': '225177'},
    {'title': 'Ягоды', 'href': f"/ru/{CITY}/catalog/cat/225562-yagody", 'catalog': '225562'},
    {'title': 'Соленья', 'href': f"/ru/{CITY}/catalog/cat/225445-solenya", 'catalog': '225445'},
    {'title': 'Кефир, творог, сметана', 'href': f"/ru/{CITY}/catalog/cat/225446-kefir_tvorog_smetana", 'catalog': '225446'},
    {'title': 'Йогурты, сырки, десерты', 'href': f"/ru/{CITY}/catalog/cat/225171-iogurty_syrki_deserty", 'catalog': '225171'},
    {'title': 'Яйца, масло, маргарин', 'href': f"/ru/{CITY}/catalog/cat/225245-yaica_maslo_margarin", 'catalog': '225245'},
    {'title': 'Сыр', 'href': f"/ru/{CITY}/catalog/cat/20160-syr", 'catalog': '20160'},
    {'title': 'Сосиски, сардельки', 'href': f"/ru/{CITY}/catalog/cat/225180-sosiski_sardelki", 'catalog': '225180'},
    {'title': 'Мясные деликатесы', 'href': f"/ru/{CITY}/catalog/cat/225451-myasnye_delikatesy", 'catalog': '225451'},
    {'title': 'Курица, индейка и птица', 'href': f"/ru/{CITY}/catalog/cat/225173-kurica_indeika_i_ptica", 'catalog': '225173'},
    {'title': 'Полуфабрикаты и маринады', 'href': f"/ru/{CITY}/catalog/cat/225609-polufabrikaty_i_marinady", 'catalog': '225609'},
    {'title': 'Морепродукты', 'href': f"/ru/{CITY}/catalog/cat/225174-moreprodukty", 'catalog': '225174'},
    {'title': 'Икра и закуски', 'href': f"/ru/{CITY}/catalog/cat/225753-ikra_i_zakuski", 'catalog': '225753'},
    {'title': 'Полуфабрикаты', 'href': f"/ru/{CITY}/catalog/cat/225184-polufabrikaty", 'catalog': '225184'},
    {'title': 'Самса, пирожки, чебуреки', 'href': f"/ru/{CITY}/catalog/cat/225187-samsa_pirozhki_chebureki", 'catalog': '225187'},
    {'title': 'Фрукты и овощи замороженные', 'href': f"/ru/{CITY}/catalog/cat/225189-frukty_i_ovoshi_zamorozhennye", 'catalog': '225189'},
    {'title': 'Хлеб, выпечка, пироги и тесто', 'href': f"/ru/{CITY}/catalog/cat/225186-hleb_vypechka_pirogi_i_testo", 'catalog': '225186'},
    {'title': 'Газировка и энергетики', 'href': f"/ru/{CITY}/catalog/cat/20784-gazirovka_i_energetiki", 'catalog': '20784'},
    {'title': 'Холодный чай, компот, морс', 'href': f"/ru/{CITY}/catalog/cat/184573-holodnyi_chai_kompot_mors", 'catalog': '184573'},
    {'title': 'Соки и нектары', 'href': f"/ru/{CITY}/catalog/cat/20739-soki_i_nektary", 'catalog': '20739'},
    {'title': 'Чипсы', 'href': f"/ru/{CITY}/catalog/cat/225604-chipsy", 'catalog': '225604'},
    {'title': 'Закуски и снеки', 'href': f"/ru/{CITY}/catalog/cat/225605-zakuski_i_sneki", 'catalog': '225605'},
    {'title': 'Бакалея органическая', 'href': f"/ru/{CITY}/catalog/cat/224944-bakaleya_organicheskaya", 'catalog': '224944'},
    {'title': 'Напитки', 'href': f"/ru/{CITY}/catalog/cat/224951-napitki", 'catalog': '224951'},
    {'title': 'Овощи, орехи, сухофрукты', 'href': f"/ru/{CITY}/catalog/cat/225645-ovoshi_orehi_suhofrukty", 'catalog': '225645'},
    {'title': 'Косметика и уход', 'href': f"/ru/{CITY}/catalog/cat/225670-kosmetika_i_uhod", 'catalog': '225670'},
    {'title': 'Без глютена и лактозы', 'href': f"/ru/{CITY}/catalog/cat/224992-bez_glyutena_i_laktozy", 'catalog': '224992'},
    {'title': 'Диабетическое питание', 'href': f"/ru/{CITY}/catalog/cat/224652-diabeticheskoe_pitanie", 'catalog': '224652'},
    {'title': 'Веган продукты', 'href': f"/ru/{CITY}/catalog/cat/224663-vegan_produkty", 'catalog': '224663'},
    {'title': 'Спортивное питание', 'href': f"/ru/{CITY}/catalog/cat/225182-sportivnoe_pitanie", 'catalog': '225182'},
    {'title': 'Выпечка', 'href': f"/ru/{CITY}/catalog/cat/225179-vypechka", 'catalog': '225179'},
    {'title': 'Лаваши и лепешки', 'href': f"/ru/{CITY}/catalog/cat/225452-lavashi_i_lepeshki", 'catalog': '225452'},
    {'title': 'Вторые блюда', 'href': f"/ru/{CITY}/catalog/cat/225201-vtorye_blyuda", 'catalog': '225201'},
    {'title': 'Салаты, супы', 'href': f"/ru/{CITY}/catalog/cat/225572-salaty_supy", 'catalog': '225572'},
    {'title': 'Сэндвичи и круассаны', 'href': f"/ru/{CITY}/catalog/cat/225577-sendvichi_i_kruassany", 'catalog': '225577'},
    {'title': 'Десерты', 'href': f"/ru/{CITY}/catalog/cat/225303-deserty", 'catalog': '225303'},
    {'title': 'Правильное питание', 'href': f"/ru/{CITY}/catalog/cat/225495-pravilnoe_pitanie", 'catalog': '225495'},
    {'title': 'Чай', 'href': f"/ru/{CITY}/catalog/cat/225447-chai", 'catalog': '225447'},
    {'title': 'Печенье, вафли, пряники', 'href': f"/ru/{CITY}/catalog/cat/225042-pechene_vafli_pryaniki", 'catalog': '225042'},
    {'title': 'Шоколад, батончики, паста', 'href': f"/ru/{CITY}/catalog/cat/225247-shokolad_batonchiki_pasta", 'catalog': '225247'},
    {'title': 'Конфеты, зефир, мармелад', 'href': f"/ru/{CITY}/catalog/cat/225041-konfety_zefir_marmelad", 'catalog': '225041'},
    {'title': 'Варенье, мед, джемы, сиропы', 'href': f"/ru/{CITY}/catalog/cat/225248-varene_med_dzhemy_siropy", 'catalog': '225248'},
    {'title': 'Крупы, бобовые', 'href': f"/ru/{CITY}/catalog/cat/224398-krupy_bobovye", 'catalog': '224398'},
    {'title': 'Консервация', 'href': f"/ru/{CITY}/catalog/cat/20205-konservaciya", 'catalog': '20205'},
    {'title': 'Масло растительное', 'href': f"/ru/{CITY}/catalog/cat/225448-maslo_rastitelnoe", 'catalog': '225448'},
    {'title': 'Майонез, кетчуп, горчица', 'href': f"/ru/{CITY}/catalog/cat/224588-maionez_ketchup_gorchica", 'catalog': '224588'},
    {'title': 'Соусы и уксусы', 'href': f"/ru/{CITY}/catalog/cat/225450-sousy_i_uksusy", 'catalog': '225450'},
    {'title': 'Сахар, соль, специи', 'href': f"/ru/{CITY}/catalog/cat/224402-sahar_sol_specii", 'catalog': '224402'},
    {'title': 'Сухие завтраки', 'href': f"/ru/{CITY}/catalog/cat/224533-suhie_zavtraki", 'catalog': '224533'},
    {'title': 'Продукты быстрого приготовления', 'href': f"/ru/{CITY}/catalog/cat/25400-produkty_bystrogo_prigotovleniya", 'catalog': '25400'},
    {'title': 'Мука, ингредиенты для выпечки', 'href': f"/ru/{CITY}/catalog/cat/225181-muka_ingredienty_dlya_vypechki", 'catalog': '225181'},
    {'title': 'Аксессуары для кормления', 'href': f"/ru/{CITY}/catalog/cat/224624-aksessuary_dlya_kormleniya", 'catalog': '224624'},
    {'title': 'Подгузники и гигиена', 'href': f"/ru/{CITY}/catalog/cat/25414-podguzniki_i_gigiena", 'catalog': '25414'},
    {'title': 'Игрушки, книги и досуг', 'href': f"/ru/{CITY}/catalog/cat/224620-igrushki_knigi_i_dosug", 'catalog': '224620'},
    {'title': 'Канцелярия', 'href': f"/ru/{CITY}/catalog/cat/21969-kancelyariya", 'catalog': '21969'},
    {'title': 'Средства для мытья посуды', 'href': f"/ru/{CITY}/catalog/cat/224494-sredstva_dlya_mytya_posudy", 'catalog': '224494'},
    {'title': 'Стирка и уход за бельём', 'href': f"/ru/{CITY}/catalog/cat/224405-stirka_i_uhod_za_bel_m", 'catalog': '224405'},
    {'title': 'Для уборки', 'href': f"/ru/{CITY}/catalog/cat/225190-dlya_uborki", 'catalog': '225190'},
    {'title': 'Посуда и товары для кухни', 'href': f"/ru/{CITY}/catalog/cat/224988-posuda_i_tovary_dlya_kuhni", 'catalog': '224988'},
    {'title': 'Полезные мелочи', 'href': f"/ru/{CITY}/catalog/cat/225211-poleznye_melochi", 'catalog': '225211'},
    {'title': 'Для декора', 'href': f"/ru/{CITY}/catalog/cat/225502-dlya_dekora", 'catalog': '225502'},
    {'title': 'Для дачи и пикника', 'href': f"/ru/{CITY}/catalog/cat/225370-dlya_dachi_i_piknika", 'catalog': '225370'},
    {'title': 'Товары для праздников', 'href': f"/ru/{CITY}/catalog/cat/225432-tovary_dlya_prazdnikov", 'catalog': '225432'},
    {'title': 'Макияж', 'href': f"/ru/{CITY}/catalog/cat/225251-makiyazh", 'catalog': '225251'},
    {'title': 'Уход за волосами', 'href': f"/ru/{CITY}/catalog/cat/224409-uhod_za_volosami", 'catalog': '224409'},
    {'title': 'Уход за лицом', 'href': f"/ru/{CITY}/catalog/cat/224583-uhod_za_licom", 'catalog': '224583'},
    {'title': 'Уход за полостью рта', 'href': f"/ru/{CITY}/catalog/cat/224413-uhod_za_polostyu_rta", 'catalog': '224413'},
    {'title': 'Уход за телом', 'href': f"/ru/{CITY}/catalog/cat/21687-uhod_za_telom", 'catalog': '21687'},
    {'title': 'Для собак', 'href': f"/ru/{CITY}/catalog/cat/202170-dlya_sobak", 'catalog': '202170'},
    {'title': 'Для других питомцев', 'href': f"/ru/{CITY}/catalog/cat/225493-dlya_drugih_pitomcev", 'catalog': '225493'},
    {'title': 'Гигиена и уход за животными', 'href': f"/ru/{CITY}/catalog/cat/202652-gigiena_i_uhod_za_zhivotnymi", 'catalog': '202652'},
]

URL_FST = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?&limit=40&token="
URL_NXT = f"https://arbuz.kz/api/v1/shop/catalog/{SUB_CATALOG}?page={PAGE}&limit=40&token="

# -------------- изменяемое -- начало------
PARAMS = {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9",
    "content-type": "application/json",
    "cookie": "PHPSESSID=92a8548b16703e683904dc3eed108e4a; __cf_bm=142EiNoLkB75Cpx1ow7_c8DqxJSAqzGCWKzwW8covOc-1748495039-1.0.1.1-HYg3SsZBeNIvKy2e9c5eNs_5bHcOMc9xfspRWGaLifqQRoD4Ldd5FxISBPYj0_kyBU1ook9v8ZIZ3UuIg9Mq36hJzTNDpjH5aDoXagci6o4; _gcl_au=1.1.2048657469.1748495042; arbuz-kz_jwt_v3=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYjRkOTdmNC02OTM3LTRjNzMtYmI1My03ZTY5ZjYxM2RjM2IiLCJpc3MiOiJBTjRjR0FRampGY2dDN3RaaXNlaklMd1hzam1VWExQdyIsImlhdCI6MTc0ODQ5NTA0MywiZXhwIjo0OTAyMDk1MDQzLCJjb25zdW1lciI6eyJpZCI6ImYxYTRkOGY5LTU1ZDctNDIzNi05YmRhLTBjZmFmNGQ2NDdjZiIsIm5hbWUiOiJhcmJ1ei1rei53ZWIuZGVza3RvcCJ9LCJjaWQiOm51bGx9.-VcOh9YnB3nORNWSDqpXUvrAOifRd9fS00_1t5YBlWE; _gid=GA1.2.1464998987.1748495043; _fbp=fb.1.1748495043280.917971049606570219; _ym_uid=1748495043283419558; _ym_d=1748495043; _ym_isad=2; _tt_enable_cookie=1; _ttp=01JWD6T2Z8ZPW4QX1J4WAMY1PD_.tt.1; _ym_visorc=w; __stripe_mid=a9b2c30f-7689-45e1-8667-064c9018c3d2b74b0e; __stripe_sid=9541e6fb-02a2-404e-b1e3-c2afb3b42343e3c76f; _ga=GA1.1.327576258.1748495043; ttcsid=1748495043564::Sob2HaAnFKv-VqstXGeO.1.1748495088452; ttcsid_C3LVC6VB3D4L4OG4N5JG=1748495043563::7STRx9lg1_SWwlOjAibV.1.1748495208733; ttcsid_CHF1FEBC77UAIJ1A1D70=1748495043564::J10BTi7NVphRXbR71gr-.1.1748495208733; _ga_0X26SLE0CQ=GS2.1.s1748495042$o1$g1$t1748495221$j20$l0$h0; amp_9e7fe7=iypa0Mw-p1CgaXrysyYpHe...1isd6q13a.1isd6vhfv.0.0.0",
    "priority": "u=1, i",
    "referer": f"https://arbuz.kz{HREF}",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-locale": "ru"
  },
  "referrer": f"https://arbuz.kz{HREF}",
  "referrerPolicy": "same-origin",
  "body": None,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
};

# -------------- изменяемое -- конец------
###############
