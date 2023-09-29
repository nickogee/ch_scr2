import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
import scr.magnum_api_scraper as mgm
import scr.airba_api_scraper as air
import datetime


def run_fast_scrapers():

    if datetime.datetime.today().weekday() == 7:
        try:
            abz.fast_category_scraper()
        except Exception as ex:
            print(ex)
        
        try:
            glv.fast_category_scraper()
        except Exception as ex:
            print(ex)

        try:
            mgm.fast_category_scraper()
        except Exception as ex:
            print(ex)
            
        try:
            air.fast_category_scraper()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    run_fast_scrapers()