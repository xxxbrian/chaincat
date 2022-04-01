import requests
from src.config import URL
import pandas as pd
import time


def get_df_by_api(path, params) -> pd.DataFrame:
    res = requests.get(f'{URL}{path}', params=params)
    return pd.read_json(res.text, convert_dates=['t'])


def get_list_by_key(df: pd.DataFrame, key: str = 'v') -> list:
    return [i for i in df[key]]


def get_median_of_list(l: list) -> int:
    sort_l = sorted(l)
    return sort_l[int(len(l) / 2)]


def last_n_year(n: int) -> int:
    return last_n_day(365*n)
    # return int(time.time() - (31536000 * n))


def last_n_month(n: int) -> int:
    return last_n_day(30*n)
    # return int(time.time() - (2678400 * n))


def last_n_week(n: int) -> int:
    return last_n_day(7*n)
    # return int(time.time() - (604800 * n))


def last_n_day(n: int) -> int:
    return last_n_hours(24*n)
    # return int(time.time() - (86400 * n))

def last_n_hours(n: int) -> int:
    return int(time.time() - (3600 * n))
