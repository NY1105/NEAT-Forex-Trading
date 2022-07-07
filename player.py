class Player:

    def __init__(self, name, df):
        self.name = name                # name       :  the name of the player
        self.last_order_index = -1      # record     :  store the row of the trading in excel
        self.cash_total = 1000000       # cash total :  the initial cash amount of the player
        self.size = 1000                # lot size   :  for each lot the player invest with size of 10
        self.df = df                    # df         :  it is the dataframe
        self.position = 0               # position   :  -1 sell, 0 no order, 1 buy

    def buy(self, index):  # open buy order
        if self.position == 0:              # if no order exist
            self.last_order_index = index   # record the index during order made
            self.position = self.size
        else:
            print("order existed, cannot open buy order")  # error exist

    def sell(self, index):  # open sell order
        if self.position == 0:              # if no order exists
            self.last_order_index = index   # record the index during order made
            self.position = -self.size
        else:
            print("order existed, cannot open sell order")  # error exist

    def close_order(self, index):  # calculating profit during trade
        if self.position > 0:  # close buy order
            last_price = self.df['Close'].iloc[self.last_order_index]
            curr_price = self.df['Close'].iloc[self.index]
            profit = self.position * (curr_price - last_price)  # calculation of buy profit
        elif self.position < 0:  # close sell order
            last_price = self.df['Close'].iloc[self.last_order_index]
            curr_price = self.df['Close'].iloc[self.index]
            profit = self.position * (curr_price - last_price)  # calculation of sell profit
        self.cash_total += profit
        self.position = 0
