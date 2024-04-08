import pandas as pd
from datetime import datetime, timedelta

def get_dur(d1: str, d2: str):
    date1 = datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
    return (date2 - date1).seconds // 60

def get_cost(d1: str, dur: int, promo: int):
    date1 = datetime.strptime(d1, '%Y-%m-%d %H:%M:%S')
    res = 0
    if not promo:
        res += 30
    if 0 <= date1.weekday() <= 4:
        if 1 <= date1.hour <= 5:
            res += dur * 3
        elif 6 <= date1.hour <= 9:
            res += dur * 4
        elif 10 <= date1.hour <= 15:
            res += dur * 5
        elif 16 <= date1.hour <= 21:
            res += dur * 6
        else:
            res += dur * 5
    else:
        if 1 <= date1.hour <= 5:
            res += dur * 3
        elif 6 <= date1.hour <= 9:
            res += dur * 4
        elif 10 <= date1.hour <= 15:
            res += dur * 6
        elif 16 <= date1.hour <= 21:
            res += dur * 7
        else:
            res += dur * 8
    return res


df = pd.read_csv('rides.csv', sep=',', encoding='utf-8')
df = df[~(df['start_date'].isna() | df['end_date'].isna())]
df['drive_dur'] = df.apply(lambda row: get_dur(*row[['start_date', 'end_date']]), axis=1)
df['drive_cost'] = df.apply(lambda row: get_cost(*row[['start_date', 'drive_dur', 'promo']]), axis=1)
df.to_csv('rides.csv', encoding='windows-1251')
