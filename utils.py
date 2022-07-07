import math

def sigmoid(x):
    return (2 / (1 + math.e**(-x))) - 1

def rsi(df, periods=14):
    close_delta = df['Adj Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.rolling(window=periods, adjust=False).mean()
    ma_down = down.rolling(window=periods, adjust=False).mean()
    return 100 - (100/(1 + ma_up / ma_down))