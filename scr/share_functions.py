import requests
import time
import random


def disc(st_df):
    if st_df.pricePrevious:
        return st_df.pricePrevious - st_df.priceActual
    else:
        return 0


def disc_prercent(st_df):
    if st_df.discount:
        return round(st_df.discount / st_df.pricePrevious * 100, 2)
    else:
        return 0


def get_fetch(url, params):
    headers = params.get('headers')
    method = params.get('method')
    body = params.get('body')
    resp_params = params.get('params')

    if method == 'POST':      
        return requests.post(url=url, headers=headers, data=body)
    elif method == 'GET':
        return requests.get(url=url, headers=headers, params=resp_params)


def rand_pause(add_sec = 0):
        time.sleep(15 + random.randint(-10, 15) + add_sec)
        # time.sleep(5 + random.randint(0, 5) + add_sec)


def format_name(raw_name:str):
    name_ls = [i for i in raw_name if i.isalpha() or i in [' ', '-', '/', '_']]
    name = ''.join(name_ls)
    name = name.strip()
    return name.capitalize()

