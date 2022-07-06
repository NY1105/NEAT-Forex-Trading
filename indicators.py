from textwrap import indent
import pandas as pd

df = pd.read_csv ('EURUSD.csv')
df['FastSMA'] = df['Close'].rolling(7, min_periods=7).sum().fillna(df['Close'])
df['SlowSMA'] = df['Close'].rolling(20, min_periods=20).sum().fillna(df['Close'])

class Indicators:        

    def get_volume(self, time):
        return df['Volume(Millions)'].iloc[time]
    
    def get_close_price(self, time):
        return df['Close'].iloc[time]

    def get_df(self):
        return df    

    def get_SMA_diff(self, time):
        return df['FastSMA'].iloc[time]-df['SlowSMA'].iloc[time]

