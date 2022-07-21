import pandas as pd
from fetch import *
from datetime import date
from utils import *
from collections import deque

SYMBOL = 'EURUSD'
START_DATE = date(2022, 6, 20)
END_DATE = date(2022, 6, 24)
MODE = 'train'
# fetch([SYMBOL], START_DATE, END_DATE)


class Indicators:
    def __init__(self,mode):

        self.df = pd.read_csv(f'data/csv/{SYMBOL}/_{SYMBOL}_{mode}.csv')
        # self.df['FastSMA'] = self.df['Close'].rolling(50, min_periods=50).mean().fillna(self.df['Close'])
        # self.df['SlowSMA'] = self.df['Close'].rolling(100, min_periods=100).mean().fillna(self.df['Close'])
        self.df['ClosePct'] = self.df['Close'].pct_change(fill_method='ffill')
        self.df['VolumePct'] = self.df['Volume'].pct_change(fill_method='ffill')
        self.df.drop(self.df[self.df.Volume == 0].index, inplace=True)
        # self.df['RSI'] = rsi(self.df)
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.closes = deque()
        self.volumes = deque()

    def get_df(self):
        return self.df

    def get_volume(self, index):
        return self.df['Volume'].iloc[index]

    def get_close(self, index):
        return self.df['Close'].iloc[index]

    def get_trend(self, index, lookback=30):
        if index < lookback:
            return 0
        return sigmoid((self.df['Close'].iloc[index - lookback] - self.df['Close'].iloc[index]) / lookback)

    def get_price_diff_with_prev(self, index):
        if index < 1:
            return 0
        return ((self.df['Close'].iloc[index] - self.df['Close'].iloc[index - 1]) / self.df['Close'].iloc[index - 1])

    def get_rsi(self, index):
        return self.df['RSI'].iloc[index]

    def get_sma_diff_pct(self, index):
        return (self.df['FastSMA'].iloc[index] - self.df['SlowSMA'].iloc[index]) / self.df['SlowSMA'].iloc[index]

    def get_past_data(self, index, lookback=10):
        if len(self.closes) < lookback:
            self.closes = deque(0 for i in range(lookback))
            self.closespct = deque(0 for i in range(lookback))
            self.volumes = deque(0 for i in range(lookback))
            self.volumespct = deque(0 for i in range(lookback))
        self.closes.popleft()
        self.closes.append(self.df['Close'].iloc[index])
        self.closespct.popleft()
        self.closespct.append(self.df['ClosePct'].iloc[index])
        self.volumes.popleft()
        self.volumes.append(self.df['Volume'].iloc[index])
        self.volumespct.popleft()
        self.volumespct.append(self.df['VolumePct'].iloc[index])
        return self.closes, self.volumes, self.closespct, self.volumespct
