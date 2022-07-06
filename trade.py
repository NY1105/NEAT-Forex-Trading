from tokenize import Double


class Trade:

    def __init__(self, cash_total: float, action: str):
        self.cash_total = cash_total
        self.action = action

    def open_order(self):  # open order - - buy/sell
        pass

    def close_order(self):  # calculating profit
        pass
