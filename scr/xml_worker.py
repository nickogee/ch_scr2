from constants.constants import UPLOAD_FOLDER, MERCANTS, DB_ROW_DATA_COLUMNS_LS, DB_PATH, DB_ROW_DATA_TABLE
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
from scr.database_worker import read_mercant_data


def create_xml_str(result: list):
    current_date = datetime.now()

    # 1 lvl
    yml_catalog = ET.Element('yml_catalog', {'date': str(current_date.isoformat())})

    # 2 lvl
    shop = ET.SubElement(yml_catalog, 'shop')
    
    # 3 lvl
    name = ET.SubElement(shop, 'name')
    name.text = result[0]['mercant_name']

    company = ET.SubElement(shop, 'company')
    company.text = result[0]['mercant_id']

    categories = ET.SubElement(shop, 'categories')
    categories.text = ''
    
    offers =  ET.SubElement(shop, 'offers')

    for offer_dct in result:
        # 4 lvl
        offer = ET.SubElement(offers, 'offer', {'id': offer_dct['product_id']})

        # 5 lvl
        name = ET.SubElement(offer, 'name')
        name.text = offer_dct['title']
        
        url = ET.SubElement(offer, 'url')
        url.text = offer_dct['url']
        
        price = ET.SubElement(offer, 'price')
        try:
            price.text = str(int(offer_dct['cost']))
        except Exception as ex:
            price.text = '0'
            print(ex)
        
        oldprice = ET.SubElement(offer, 'oldprice')
        try:
            oldprice.text = str(int(offer_dct['prev_cost']))
        except Exception as ex:
            oldprice.text = '0'
            print(ex)
          
        path = ET.SubElement(offer, 'path')
        path.text = offer_dct['category_full_path']
        
        category = ET.SubElement(offer, 'category')
        category.text = offer_dct['sub_category']
        
        picture = ET.SubElement(offer, 'picture')
        picture.text = offer_dct['url_picture']
        
        scrappedat = ET.SubElement(offer, 'scrappedat')
        scrappedat.text = offer_dct['time_scrap']

        measure = ET.SubElement(offer, 'measure')
        measure.text = offer_dct['measure']

        measure = ET.SubElement(offer, 'city')
        measure.text = offer_dct['city']
        

    tree = ET.ElementTree(yml_catalog)
    file_name = f"{UPLOAD_FOLDER}{result[0]['mercant_id']}.xml"
    tree.write(file_or_filename=file_name, 
               encoding='utf-8', 
               xml_declaration=True, 
               short_empty_elements=False)


def datetime_str_to_obj(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    if not us:
        us = 0
    else:
        us = int(us.rstrip("Z"), 10)
    
    return dt + timedelta(microseconds=us)


def make_data_file():

    columns_str = ', '.join(DB_ROW_DATA_COLUMNS_LS)
    for key in MERCANTS.keys():
        filter_tpl = ('mercant_id', MERCANTS[key])
        db_result = read_mercant_data(db_path=DB_PATH, table_name=DB_ROW_DATA_TABLE, columns=columns_str, filter_tpl=filter_tpl)

        if db_result:

            result = []
            for dt_line in db_result:
                timestamp = datetime_str_to_obj(dt_line[12])
                now = datetime.now()
                delta = now - timestamp
                days = delta.days

                if days <= 7:
                    ln_dct = {DB_ROW_DATA_COLUMNS_LS[i]: dt_line[i] for i in range(0, len(DB_ROW_DATA_COLUMNS_LS))}
                
                    result.append(ln_dct)

            if result:
                create_xml_str(result)
            else:
                print(f'Нет данных в базе для выгрузки в xml, для {key}')
        



if __name__ == "__main__":
    make_data_file()




