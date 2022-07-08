import pandas as pd


class Indicators:
    def __init__(self):
        self.df = pd.read_csv('EURUSD.csv')
        self.df['FastSMA'] = self.df['Close'].rolling(50, min_periods=50).mean().fillna(self.df['Close'])
        self.df['SlowSMA'] = self.df['Close'].rolling(100, min_periods=100).mean().fillna(self.df['Close'])
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def get_df(self):
        return self.df

    def get_volume(self, index):
        return self.df['Volume(Millions)'].iloc[index]

    def get_ma_diff(self, index):
        return self.df['FastSMA'].iloc[index] - self.df['SlowSMA'].iloc[index]

    def get_close(self, index):
        return self.df['Close'].iloc[index]
