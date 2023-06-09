from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import random
import datetime
# from constants import DIR
DIR = 'ch_scr2'


CATEGORY = 'Овощи, фрукты, ягоды, грибы'
# URL = 'https://kaspi.kz/shop/c/food/?q=%3AallMerchants%3AMagnum%3AavailableInZones%3AMagnum_ZONE1'
# URL = 'https://kaspi.kz/shop/'
# URL = 'https://kaspi.kz/shop/c/beauty%20care/?q=%3AallMerchants%3AMagnum%3AavailableInZones%3AMagnum_ZONE1'
URL = 'https://2ip.ru/'

# CHROMEDRIVER = '/Users/hachimantaro/PycharmProjects/Ch_scrp/chromedriver/chromedriver'
CHROMEDRIVERPATH = f'{DIR}/CromeDriver/chromedriver'


class KaspiParser():

    def __init__(self):
        self.date_time_now = datetime.datetime.now()
        self.rezult = []
        self.driver = None
        self.options = None
        self.df = None
        self.make_driver()

    def make_driver(self):
        useragent = UserAgent()

        # options = webdriver.ChromeOptions()
        
    
        options = webdriver.ChromeOptions()
        # options.add_argument("user-agent=Mozilla/5.0 (Linux. Android ZaG; SM-6230Y BuiLd/NRD20M) AppLetebKit/532.36 (KHIML. Like Gecko).Chrome/59.0.3071.125 Mobile Safari/537.36")
        options.add_argument(f'user-agent={useragent.chrome}')
        options.add_argument ("--disable-blink-features=AutomationControlled")

        options.add_argument("--no-sandbox")
        # options.add_argument("--headless") # запуск в фоновом режиме, без открытия окна хрома
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')

        options.add_experimental_option("excludeSwitches", ["enable automation" ])
        options.add_experimental_option ('useAutomationExtension', False)
        
        driver = webdriver.Chrome(
        executable_path=CHROMEDRIVERPATH,
        options=options
            )
        
        driver.maximize_window()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", 
                       {
                           'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                           '''
                       })


        self.options = options
        self.driver = driver

    def rand_pause(self):
        time.sleep(10 + random.randint(0, 10))

    def __find_element(self, by, value):
        return self.driver.find_element(by, value)

    def __find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    def search_data(self):

        self.driver.get(URL)
        time.sleep(100)
        self.rand_pause()
        Almaty = self.__find_element(By.CSS_SELECTOR, '[data-city-id="750000000"]')
        Almaty.click()

        category_list = self.__find_elements(By.CLASS_NAME, 'tree__link')

        for category in category_list:

            # Найдена нужная категория
            if category.text == CATEGORY:
                category.click()
                self.rand_pause()

                # ищем список подкатегорий
                sub_category_list = self.__find_elements(By.CLASS_NAME, 'tree__link')

                # начиная с индекса 3 - это список подкатегорий
                for i in range(3, len(sub_category_list)):

                    if i > 3:
                        # ищем список подкатегорий занова, после каждой следующей итерации
                        sub_category_list = self.__find_elements(By.CLASS_NAME, 'tree__link')

                    sub_category = sub_category_list[i]
                    sub_category_text = sub_category.text
                    sub_category.click()
                    self.rand_pause()

                    next_page = True
                    while next_page:
                        #  Внутри категории ищем элементы с названием и ценой продуктов
                        product_list = self.__find_elements(By.CLASS_NAME, 'item-card__info')

                        for product_card in product_list:
                            title_tag = product_card.find_element(By.CLASS_NAME, 'item-card__name')
                            price_tag = product_card.find_element(By.CLASS_NAME, 'item-card__prices-price')
                            priceL = [j for j in price_tag.text if j.isdigit()]
                            l = {
                                'title': title_tag.text,
                                'sub_category': sub_category_text,
                                'category': CATEGORY,
                                'brand': '',
                                'priceActual': float(''.join(priceL)),
                                'pricePrevious': 0,
                            }

                            self.rezult.append(l)

                        next_page = self.__push_the_button_next()

                    else:
                        # ищем список элементов с категориями и подкатегориями
                        # и возвращаемся на страницу со списком подкатегорий (кликаем по основной категории)
                        sub_category_list_ = self.__find_elements(By.CLASS_NAME, 'tree__link')
                        category_ = sub_category_list_[2]
                        category_.click()
                        self.rand_pause()

                else:
                    # все данные по искомой категории просмотрены
                    break

    def __push_the_button_next(self):

        try:
            next_btn_list = self.__find_elements(By.CLASS_NAME, 'pagination__el')
            next_btn = next_btn_list[-1]
        except Exception:
            # Нет кнопок с переключением на след. страницу - это единственная страница по текущей подкатегории
            return False

        try:
            disabled_btn = self.__find_element(By.CLASS_NAME, '_disabled')
        except Exception:
            disabled_btn = None

        if disabled_btn and disabled_btn == next_btn:
            return False
        else:
            next_btn.click()
            self.rand_pause()
            return True

    # def __make_DataFrame(self):
    #     self.df = make_DataFrame(self.rezult)

    # def __upload_to_excel(self):
    #     file_name = f'data_rezult/KaspiMagnum - {CATEGORY} {self.date_time_now.strftime("%d_%m_%Y")}.xlsx'
    #     upload_to_excel(self.df, file_name)

    def start(self):
        # self.make_driver()
        self.search_data()
        # self.__make_DataFrame()
        # self.__upload_to_excel()

        self.driver.close()


def main():

    kaspi = KaspiParser()
    kaspi.start()


if __name__ == '__main__':
    main()


