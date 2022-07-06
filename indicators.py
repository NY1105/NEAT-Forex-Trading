import pandas as pd

df = pd.read_csv ('EURUSD.csv')

class Indicators:

    def __init__(self, time):
        self.time = time
        df['SMA'] = df['Close'].rolling(20, min_periods=20).fillna(df['Close'])

    def get_volume(self):
        return df['Volume(Millions)'].iloc[self.time]
    
    def get_close_price(self):
        return df['Close'].iloc[self.time]

    def get_df(self):
        return df    

    def get_SMA(self):
        return df['SMA'].iloc[self.time]

