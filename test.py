import pandas as pd

SYMBOL = 'EURUSD'
MODE = 'train'

df = pd.read_csv(f'data/csv/{SYMBOL}/_{SYMBOL}_{MODE}.csv')
df['FastSMA'] = df['Close'].rolling(50, min_periods=50).mean().fillna(df['Close'])
df['SlowSMA'] = df['Close'].rolling(100, min_periods=100).mean().fillna(df['Close'])
df['ClosePct'] = df['Close'].pct_change(fill_method='ffill')
df['VolumePct'] = df['Volume'].pct_change(fill_method='ffill')
df.drop(df[df.Volume == 0].index, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

print(df)
