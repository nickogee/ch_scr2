import scr.arbuz_api_scraper as abz
import scr.glovo_api_scraper as glv
import scr.magnum_api_scraper as mgm

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
        