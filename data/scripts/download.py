import os
import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime

symbol = 'USDJPY=X'
interval = '1m'
period = '5d'
END = '2022-06-24'
# END = datetime.today()


try:
    print(symbol)
    data = yf.download(symbol, end=END, interval=interval,period=period)
    symbol = symbol[0:6]
    file = symbol + ".csv"
    data = data.dropna()
    data.to_csv('data/train/'+symbol+".csv")
except:
    print("Unable to load data for {}".format(symbol))


