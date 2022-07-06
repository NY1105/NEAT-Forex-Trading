import yfinance as yf


def main():
    df = yf.download('USDJPY=X', start='2022-06-01', end='2022-06-30').reset_index()
    return df


if __name__ == '__main__':
    main()
