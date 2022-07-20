from tracemalloc import start
import pandas as pd
from datetime import date, datetime, timedelta
from pathlib import Path
from collections import deque
import os
import math

today = (2022, 6, 30)
TRAIN = 30
TEST = 7
SYMBOL = 'EURUSD'


def sigmoid(x):
    return (2 / (1 + math.e**(-x))) - 1


def rsi(df, periods=14):
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    return 100 - (100 / (1 + ma_up / ma_down))


def param_gen(amount):

    s = ""
    for i in range(amount):
        s = s + f'price[{i}],'
    for i in range(amount):
        s = s + f'volume[{i}],'
    print(s)

    return
# param_gen(15)


def daysinwhichmonth(month: int, year):
    if month < 1:
        month += 12
    if month > 12:
        month -= 12
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        if isleap(year):
            return 29
        else:
            return 28


def isleap(year):
    if (year % 400 == 0) and (year % 100 == 0):
        return True
    elif (year % 4 == 0) and (year % 100 != 0):
        return True
    else:
        return False


def to_read(today: tuple, symbol=SYMBOL):

    curr_year, curr_month = today[0], today[1]
    last1_year, last1_month = curr_year, curr_month - 1
    last2_year, last2_month = curr_year, curr_month - 2
    next_year, next_month = curr_year, curr_month + 1
    if last1_month < 1:
        last1_year -= 1
        last1_month += 12
    if last2_month < 1:
        last2_year -= 1
        last2_month += 12
    if next_month > 12:
        next_year += 1
        next_month -= 12
    curr_path = Path(f'{symbol}_{curr_year}_{curr_month:02d}.csv')
    last1_path = Path(f'{symbol}_{last1_year}_{last1_month:02d}.csv')
    last2_path = Path(f'{symbol}_{last2_year}_{last2_month:02d}.csv')
    next_path = Path(f'{symbol}_{next_year}_{next_month:02d}.csv')
    return last2_path, last1_path, curr_path, next_path


def get_train_startend(today, training_period=TRAIN):
    curr_year, curr_month, curr_day = today[0], today[1], today[2]
    start_year, start_month, start_day = curr_year, curr_month, curr_day - training_period

    while start_day < 1:
        start_month -= 1
        start_day += daysinwhichmonth(start_month, start_year)
    if start_month < 1:
        start_year -= 1
        start_month += 12
    return (start_year, start_month, start_day), (curr_year, curr_month, curr_day)


def get_test_startend(today, testing_period=TEST):
    curr_year, curr_month, curr_day = today[0], today[1], today[2]
    end_year, end_month, end_day = curr_year, curr_month, curr_day + testing_period
    while end_day > daysinwhichmonth(end_month, end_year):
        end_day -= daysinwhichmonth(end_month, end_year)
        end_month += 1
    if end_month > 12:
        end_year += 1
        end_month -= 12
    return (curr_year, curr_month, curr_day), (end_year, end_month, end_day)


def get_deque(today, mode='train', symbol=SYMBOL):
    if mode == 'train':
        start, end = get_train_startend(today)
    if mode == 'test':
        start, end = get_test_startend(today)
    dstart, dend = date(start[0], start[1], start[2]), date(end[0], end[1], end[2])
    last2_path, last1_path, curr_path, next_path = to_read(today, symbol)
    last2df = pd.read_csv(f'data/csv/{symbol}/{last2_path}')
    last1df = pd.read_csv(f'data/csv/{symbol}/{last1_path}')
    currdf = pd.read_csv(f'data/csv/{symbol}/{curr_path}')
    nextdf = pd.read_csv(f'data/csv/{symbol}/{next_path}')
    record = False
    res = []
    indextime = []
    for i in (last2df, last1df, currdf, nextdf):  # search
        for index in range(len(i)):
            c1, c2, c3 = (i['Datetime'].iloc[index][:10]).split('-')
            c = date(int(c1), int(c2), int(c3))
            if c == dstart:
                record = True
            if c == dend:
                record = False
                break
            if record:
                indextime.append(i['Datetime'].iloc[index])
                res.append([i['Open'].iloc[index], i['High'].iloc[index], i['Low'].iloc[index], i['Close'].iloc[index], i['Volume'].iloc[index]])
                # res = pd.concat([res,i.iloc[index]])
    df = pd.DataFrame(data=res, index=indextime, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    save_name = f'_{symbol}_{mode}.csv'
    save_path = Path(f'data/csv/{symbol}')
    save_file = save_path / save_name
    save_path.mkdir(parents=True, exist_ok=True)
    if os.path.isfile(save_file):
        os.remove(save_file)
    df.to_csv(save_file)


def get_ks_deque(i, now=(2010, 3, 1, 0, 0, 0), symbol=SYMBOL):
    start_time = datetime(now[0],now[1],now[2],now[3],now[4],now[5]) - timedelta(days=30)
    if i == 0:
        end_time = start_time + timedelta(hours=1)
    if i == 1:
        end_time = start_time + timedelta(hours=2)
    if i == 2:
        end_time = start_time + timedelta(hours=4)
    if i == 3:
        end_time = start_time + timedelta(hours=8)
    if i == 4:
        end_time = start_time + timedelta(hours=24)
    if i == 5:
        end_time = start_time + timedelta(hours=72)
    if i == 6:
        end_time = start_time + timedelta(hours=168)
    last2_path, last1_path, curr_path, next_path = to_read((now[0],now[1],now[2]), symbol)
    last2df = pd.read_csv(f'data/csv/{symbol}/{last2_path}')
    last1df = pd.read_csv(f'data/csv/{symbol}/{last1_path}')
    currdf = pd.read_csv(f'data/csv/{symbol}/{curr_path}')
    nextdf = pd.read_csv(f'data/csv/{symbol}/{next_path}')
    record = False
    res = []
    indextime = []
    for i in (last2df, last1df, currdf, nextdf):  # search
        for index in range(len(i)):
            c1, c2, c3 = (i['Datetime'].iloc[index][:10]).split('-')
            c4 = (i['Datetime'].iloc[index][11:13])
            c = datetime(int(c1), int(c2), int(c3), int(c4), 0, 0)
            if c == start_time:
                record = True
            if c == end_time:
                record = False
                break
            if record:
                indextime.append(i['Datetime'].iloc[index])
                res.append([i['Open'].iloc[index], i['High'].iloc[index], i['Low'].iloc[index], i['Close'].iloc[index], i['Volume'].iloc[index]])
                # res = pd.concat([res,i.iloc[index]])
    df = pd.DataFrame(data=res, index=indextime, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
    save_name = f'_{symbol}_train.csv'
    save_path = Path('data/csv/{symbol}')
    save_file = save_path / save_name
    save_path.mkdir(parents=True, exist_ok=True)
    if os.path.isfile(save_file):
        os.remove(save_file)
    df.to_csv(save_file)


def update_date(date):
    '''
    add 7 days after training
    check if exceed month or year boundary
    curr_year, curr_month, curr_day = date[0], date[1], date[2]
    '''
    year, month, day = date
    day += 7
    have_days = daysinwhichmonth(month, year)
    if day > have_days:
        day -= have_days
        month += 1
        if month > 12:
            month -= 12
            year += 1
    return (year, month, day)


def result_checkdir(symbol=SYMBOL, mode='test'):
    save_name = f'{symbol}_{mode}_result.csv'
    save_path = Path('result/')
    save_file = save_path / save_name
    if os.path.isfile(save_file):
        os.remove(save_file)
    save_path.mkdir(parents=True, exist_ok=True)
    with open(save_file, 'w') as f:
        f.write('Index,Type,Price,Profit\n')
