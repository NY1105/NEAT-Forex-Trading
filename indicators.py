from textwrap import indent
import pandas as pd

df = pd.read_csv('EURUSD.csv')
df['FastSMA'] = df['Close'].rolling(7, min_periods=7).mean().fillna(df['Close'])
df['SlowSMA'] = df['Close'].rolling(20, min_periods=20).mean().fillna(df['Close'])


class Indicators:

    def get_volume(time):
        return df['Volume(Millions)'].iloc[time]

    def get_close_price(time):
        return df['Close'].iloc[time]

    def get_df():
        return df

    def get_SMA_diff(time):
        return df['FastSMA'].iloc[time] - df['SlowSMA'].iloc[time]
