import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
import scr.magnum_api_scraper as mgm
import scr.airba_api_scraper as air
import scr.volt_api_scraper as vlt
import scr.klever_api_scraper as kvr
import datetime
import sys
from constants.constants import CITYS_LS


def run_fast_scrapers():
    
    if datetime.datetime.today().weekday() == 6:

        if len(sys.argv) > 1:
            city_ls = [sys.argv[1],] 
        else:
            city_ls = CITYS_LS[:]

        for cur_city in city_ls:
            try:
                abz.fast_category_scraper(city=cur_city)
            except Exception as ex:
                print(ex)
        
        for cur_city in city_ls:
            try:
                mgm.fast_category_scraper(city=cur_city)
            except Exception as ex:
                print(ex)
        
        for cur_city in city_ls:
            try:
                kvr.fast_category_scraper(city=cur_city)
            except Exception as ex:
                print(ex)

        try:
            glv.fast_category_scraper()
        except Exception as ex:
            print(ex)

        try:
            air.fast_category_scraper()
        except Exception as ex:
            print(ex)
        
        try:
            vlt.fast_category_scraper()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    run_fast_scrapers()