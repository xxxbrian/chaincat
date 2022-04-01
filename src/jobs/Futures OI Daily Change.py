import json
import numpy as np
from statistics import median
from numpy import mean
import requests
import pandas as pd
import time

API_KEY = '27B7d366MLdyKjAIP15Og5BncOj'

def Futures_OI_Daily_Change():

    FuturesOI_1d_Res = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_sum',
            params={
                'a': 'BTC',
                'api_key': API_KEY,
                'i': '24h',
                'c': 'NATIVE',
                's':int(time.time()-31536000),
                'u':int(time.time()),
                },)
        #convert to panda dataframe
    #print(FuturesOI_1d_Res.text)
    Futures_OI_1d_df= pd.read_json(FuturesOI_1d_Res.text, convert_dates=['t'])

    #get value only
    FuturesOI_1d_df_Value = Futures_OI_1d_df['v']

    #Daily change = value of the n+1 th day - value of the n th day
    #get value of daily change,store in list
    OI_Daily_Change=[]
    for i in np.arange(0, len(FuturesOI_1d_df_Value)-2, 1):
        j = FuturesOI_1d_df_Value[i+1] - FuturesOI_1d_df_Value[i]
        OI_Daily_Change.append(j)
    
    #print(Futures_OI_1d_df)
    #print(OI_Daily_Change)
   
#def alert_threshold():
    OI_Change_1d_median = median(OI_Daily_Change)
    OI_Change_1d_stdeviation = np.std(OI_Daily_Change)

    #print("OI Change median is:", OI_Change_1d_median)
    #print("OI Standard Deviation is:",OI_Change_1d_stdeviation)




#Calculate last 24h Change by summing up all 10-min frame changes.
#def Futures_OI_last24h_Change():

    FuturesOI_10min_Res = requests.get('https://api.glassnode.com/v1/metrics/derivatives/futures_open_interest_sum',
        params={
            'a': 'BTC',
            'api_key': API_KEY,
            'i': '10m',
            'c': 'NATIVE',
            's':int(time.time()-86400),
            'u':int(time.time()),
            },)
    #convert to panda dataframe
    FuturesOI_10min_df= pd.read_json(FuturesOI_10min_Res.text, convert_dates=['t'])
    #get value only
    FuturesOI_10min_df_Value = FuturesOI_10min_df['v']
    #print(FuturesOI_10min_df_Value)

    #24h OI Change = The 144th value (the latest 10min OI) - the first value (the first 10min OI of the last 24h)
    OI_24h_Change = FuturesOI_10min_df_Value[143] - FuturesOI_10min_df_Value[0]
    #print("Last 24h Change is:", OI_24h_Change)

    #24h OI Change percentage = 24h OI Change/the first value (the first 10min OI of the last 24h)
    OI_24h_Change_Percentage = round(abs(OI_24h_Change/(FuturesOI_10min_df_Value[0]))*100,2)
    #Compare 24h Change with threshold value
    if (abs(OI_24h_Change) > OI_Change_1d_median + 1.5*OI_Change_1d_stdeviation):
        print("Alert! Last 24h Futures OI Change is:", OI_24h_Change, "BTC")
    else:
        pass

    if OI_24h_Change_Percentage > 5:
        if OI_24h_Change < 0:
            print("Alert! Last 24h Futures OI Change is -",OI_24h_Change_Percentage,"%")
        elif OI_24h_Change > 0:
            print("Alert! Last 24h Futures OI Change is ",OI_24h_Change_Percentage,"%") 
    else:
        print("No abnormality")
        pass


Futures_OI_Daily_Change()
