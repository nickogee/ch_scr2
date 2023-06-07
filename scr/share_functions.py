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
    headers = params['headers']
    body = params['body']
    method = params['method']

    if method == 'POST':
        return requests.post(url=url, headers=headers, data=body)
    elif method == 'GET':
        return requests.get(url=url, headers=headers)


def rand_pause():
        time.sleep(15 + random.randint(-10, 15))

