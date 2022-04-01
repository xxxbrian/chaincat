import json
import requests
import pandas as pd
import time

#Perp OI/MarketCap = OI/MC *100

API_KEY = '27B7d366MLdyKjAIP15Og5BncOj'
def Perp_OI_MC_Ratio():
    

    OI_Res = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_perpetual_sum',
        params={
            'a': 'BTC',
            'api_key': API_KEY,
            'i': '10m',
            's':int(time.time()-3000),
            'u':int(time.time()),
            'c': 'USD',
            },)
    MC_Res = requests.get('https://api.glassnode.com/v1/metrics/market/marketcap_usd',
        params={
            'a': 'BTC',
            'api_key': API_KEY,
            'i': '10m',
            's':int(time.time()-3000),
            'u':int(time.time()),
            },) 

    df_OI = pd.read_json(OI_Res.text, convert_dates=['t'])
    df_mc = pd.read_json(MC_Res.text, convert_dates=['t'])

    a = list(df_OI['v'])[-1]
    b = list(df_mc['v'])[-1]
    ratio = 100*a/b
 
    if ratio > 1.3:
        print("Alert! Perpetual Futures OI to Market Cap ratio is over 1.3! Now ratio is",ratio)
  

Perp_OI_MC_Ratio()