import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
import scr.magnum_api_scraper as mgm
import scr.airba_api_scraper as air

if __name__ == '__main__':
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