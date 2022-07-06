class Trade:

    def open_order(cash_total, action, record, index, df):  # open order - - buy/sell
        if record[action][0] != 0:
            record[action][1] = df['Close'].iloc[index]
            return
        record[action][0] = df['Close'].iloc[index]

    def close_order(cash_total, action, record, index, df):  # calculating profit - - close
        if record[action][1] == 0:
            return cash_total
        cash_total += cash_total * (record[action][1] - record[action][0])
        return cash_total


class Player:

    def __init__(self, name, df):
        self.name = name                               # name       :  the name of the player
        self.record = {'buy': [0, 0], 'sell': [0, 0]}  # record     :  store the row of the trading
        self.__cash_total = 1000                       # cash total :  the initial cash amount of the player
        self.df = df                                   # df         :  it is the dataframe

    def get_cash_total(self):  # the cash flow of the player
        return self.__cash_total

    def order_execute(self, action, index):  # the execution call for the trade
        if self.action in ('buy', 'sell'):
            Trade.open_order(self.__cash_total, action, self.record, index, self.df)
        elif self.action == 'close':
            self.__cash_total = Trade.close_order(self.__cash_total, action, self.record, index, self.df)
