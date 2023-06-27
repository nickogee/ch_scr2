from selenium import webdriver
import time
import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
from scr.database_worker import update_parent_category_mgm
from constants.constants import DB_PATH, DB_MGM_CATEGORY_TABLE, DB_MGM_CATEGORY_CREATE_STR, MERCANTS, \
                                DB_ROW_DATA_CREATE_STR, DB_ROW_DATA_TABLE



def run_webdriver():
    url = "https://arbuz.kz/#/"
    options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

    options.add_argument("user-agent Mozilla/5.0 (Linux. Android ZaG; SM-6230Y BuiLd/NRD20M) AppLetebKit/532.36 (KHIML. Like Gecko).Chrome/59.0.3071.125 Mobile Safari/537.36")

    options.add_argument ("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable automation" ])
    options.add_experimental_option ('useAutomationExtension', False)

    driver = webdriver.Chrome(
        executable_path='/Users/hachimantaro/Repo/Ch_Scr/Ch_Scr/CromeDriver/chromedriver',
        options=options
    )

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


    try:
        driver.get(url=url)
        time.sleep(500)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def run_test_case():

    filter_tpl = ('parent_id', '1107')
    update_parent_category_mgm(DB_PATH, DB_MGM_CATEGORY_TABLE, pk_column='id', filter_tpl=filter_tpl) 
    

    
if __name__ == '__main__':
    run_test_case()

