import pandas as pd
from fetch import *
from datetime import date
from utils import *

SYMBOL = 'EURUSD'
START_DATE = date(2022, 6, 14)
END_DATE = date(2022, 6, 24)
#fetch([SYMBOL], START_DATE, END_DATE)


class Indicators:
    def __init__(self):

        # self.df = pd.read_csv(f'{SYMBOL}.csv')
        self.df = pd.read_csv(f'data/csv/{SYMBOL}.csv')
        self.df['FastSMA'] = self.df['Close'].rolling(50, min_periods=50).mean().fillna(self.df['Close'])
        self.df['SlowSMA'] = self.df['Close'].rolling(100, min_periods=100).mean().fillna(self.df['Close'])
        self.df['RSI'] = rsi(self.df)
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

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
        closes = []
        volumes = []
        for tf in range(index - lookback - 1, index + 1):
            if tf < 0:
                closes.append(0)
                volumes.append(0)
            else:
                closes.append(self.df['Close'].iloc[tf])
                volumes.append(self.df['Volume'].iloc[tf])
        return closes, volumes
