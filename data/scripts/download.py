import os
import pathlib
import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime

################################################################################################################
symbol = 'USDJPY=X'
interval = '1m'
start = datetime.today() - timedelta(days=29) # start = '2022-06-20'
end = start + timedelta(days=5) # end = datetime(int(start[:4]),int(start[5:7]),int(start[8:])) + timedelta(days=5)
################################################################################################################

path = pathlib.PurePath(pathlib.Path('download.py').parent.absolute(), 'data', 'train')
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

try:
    print(symbol)
    data = yf.download(symbol, start=start, end=end, interval=interval)
    symbol = symbol[0:6]
    file = symbol + ".csv"
    data = data.dropna()
    data.to_csv('data/train/'+symbol+".csv")
except Exception as e:
    print(e)
    print("Unable to load data for {}".format(symbol))

