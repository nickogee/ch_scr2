import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
import scr.magnum_api_scraper as mgm
import scr.airba_api_scraper as air

if __name__ == '__main__':
    try:
        abz.main()
    except Exception as ex:
        print(ex)
    
    try:
        glv.main()
    except Exception as ex:
        print(ex)

    try:
        mgm.main()
    except Exception as ex:
        print(ex)
           
    try:
        air.main()
    except Exception as ex:
        print(ex)
        