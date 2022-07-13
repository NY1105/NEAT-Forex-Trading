import math
import pandas as pd


def sigmoid(x):
    return (2 / (1 + math.e**(-x))) - 1


def rsi(df, periods=14):
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    return 100 - (100 / (1 + ma_up / ma_down))


def param_gen(amount):

    # for i in range(amount):
    #     print(f'price[{i}]\nvolume[{i}],')

    for i in range(amount):
        print(f'price[{i}],')
    for i in range(amount):
        print(f'volume[{i}],')
    return


# param_gen(60)
