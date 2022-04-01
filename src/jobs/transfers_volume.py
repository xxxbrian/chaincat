import requests
import pandas as pd
import time
from src.other import *
from src.config import API_KEY


def tran_sum():
    # insert your API key here
    API_KEY = '24mwEylg8dznA5o3a8xdm6y42lE'

    # make API request
    #
    res1 = requests.get(
        'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_sum',
        params={
            'a': 'BTC',
            'api_key': API_KEY,
            'i': '10m',
            's': int(time.time() - 86400),
            'u': int(time.time()),
        },
    )

    res2 = requests.get(
        'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_sum',
        params={
            'a': 'BTC',
            'api_key': API_KEY,
            's': int(time.time() - 31536000),
            'u': int(time.time()),
        },
    )

    print(res1, res2)
    df1 = pd.read_json(res1.text, convert_dates=['t'])
    df2 = pd.read_json(res2.text, convert_dates=['t'])
    print(df1, df2)

    all365 = [i for i in df2['v']]
    all365.sort()
    threshold = all365[int(len(all365) / 2)] * 2
    print('@@@@',max(all365))

    today_v = [i for i in df1['v']]
    today_sum = sum(today_v)

    print(f'Today total is {today_sum}')
    print(f'Threshold is {threshold}')

    if today_sum > threshold:
        return True
    else:
        return False


def transfers_volume():
    path = '/transactions/transfers_volume_sum'
    list_year_volume = get_list_by_key(
        get_df_by_api(path,
                      params={
                          'a': 'BTC',
                          'api_key': API_KEY,
                          's': last_n_year(1),
                          'u': last_n_year(0),
                      }))
    list_24h_volume = get_list_by_key(
        get_df_by_api(path,
                      params={
                          'a': 'BTC',
                          'api_key': API_KEY,
                          'i': '10m',
                          's': last_n_hours(24),
                          'u': last_n_hours(0),
                      }))
    threshold = get_median_of_list(list_year_volume) * 2
    sum_24h = sum(list_24h_volume)
    return {
        'status': sum_24h > threshold,
        '24h volume': sum_24h,
        'threshold':threshold,
    }

if __name__ == '__main__':
    print(transfers_volume())