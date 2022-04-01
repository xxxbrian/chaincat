import json
from statistics import median
import requests
import pandas as pd
import time
import numpy as np
def Stablecoins_Exchange_Netflow():
    API_KEY = '27B7d366MLdyKjAIP15Og5BncOj'

    # 24h 
    # USDT
    res_usdt = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_exchanges_net',
    params={
        'a': 'USDT',
        'api_key': API_KEY,
        'i': '24h',
        's':int(time.time()-31536000),
        'u':int(time.time()),
            },)

    # USDC
    res_usdc = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_exchanges_net',
    params={
        'a': 'USDC',
        'api_key': API_KEY,
        'i': '24h',
        's':int(time.time()-31536000),
        'u':int(time.time()),
            },)

    #BUSD
    res_busd = requests.get('https://api.glassnode.com/v1/metrics/transactions/transfers_volume_exchanges_net',
    params={
        'a': 'BUSD',
        'api_key': API_KEY,
        'i': '24h',
        's':int(time.time()-31536000),
        'u':int(time.time()),
            },)


    print(res_usdt,res_usdc,res_busd)
    df_usdt = pd.read_json(res_usdt.text, convert_dates=['t'])
    df_usdc = pd.read_json(res_usdc.text, convert_dates=['t'])
    df_busd = pd.read_json(res_busd.text, convert_dates=['t'])
    #print(df_usdt,df_usdc,df_busd)

    BalanceList = [a+b+c for a,b,c in zip(df_usdt['v'],df_usdc['v'],df_busd['v'])]
    #print(mylist)
    #print(np.std(mylist))

    med = median(BalanceList) 
    #print(med)

    if BalanceList[-1] < med - np.std(BalanceList)*2:
        print('Alert! Stablecoins Exchange Large outflow; outflow value=', abs(BalanceList[-1]) )
    elif BalanceList[-1] > med + np.std(BalanceList)*2:
        print('Alert! Stablecoins Exchange Large Inflow; inflow value =', BalanceList[-1])
    else:
        print('No Abnormality')
Stablecoins_Exchange_Netflow()