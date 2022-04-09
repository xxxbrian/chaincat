import pandas as pd
import numpy as np



def trend(value):

    ema15 = np.asarray(pd.DataFrame(value).ewm(span=15, adjust=False).mean())
    ema30 = np.asarray(pd.DataFrame(value).ewm(span=30, adjust=False).mean())
    ema90 = np.asarray(pd.DataFrame(value).ewm(span=90, adjust=False).mean())

    st_today_status = bool(value[-1] > ema15[-1]) #True = uptrend ; False = downtrend
    st_ytrday_status = bool(value[-2] > ema15[-2])

    mt_today_status = bool(value[-1] > ema30[-1]) #True = uptrend ; False = downtrend
    mt_ytrday_status = bool(value[-2] > ema30[-2])

    lt_today_status = bool(value[-1] > ema90[-1]) #True = uptrend ; False = downtrend
    lt_ytrday_status = bool(value[-2] > ema90[-2])
    
    st_up = 1
    mt_up = 1
    lt_up = 1

    if st_today_status != st_ytrday_status and st_today_status == True:
        st_up = 2
    elif st_today_status != st_ytrday_status and st_today_status == False:
        st_up = 3
    else:
        st_up = 1

    if mt_today_status != mt_ytrday_status and mt_today_status == True:
        mt_up = 2
    elif mt_today_status != mt_ytrday_status and mt_today_status == False:
        mt_up = 3
    else:
        mt_up = 1

    if lt_today_status != lt_ytrday_status and lt_today_status == True:
        lt_up = 2
    elif lt_today_status != lt_ytrday_status and lt_today_status == False:
        lt_up = 3
    else:
        lt_up = 1

    return st_up,mt_up,lt_up
