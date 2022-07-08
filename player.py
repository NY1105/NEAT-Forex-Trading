class Player:

    def __init__(self, df):
        self.last_order_index = -1      # record     :  store the row of the trading in excel
        self.cash_total = 1000000       # cash total :  the initial cash amount of the player
        self.size = 100000              # lot size   :  for each lot the player invest with size of 10
        self.df = df                    # df         :  it is the dataframe
        self.position = 0               # position   :  -1 sell, 0 no order, 1 buy
        self.comission = 0.000035       # comission  :  comission in pip / size

    def buy(self, index):  # open buy order
        if self.cash_total < self.size * (self.df['Close'].iloc[index] + self.comission):  # check if the player has enough money
            print("Not enough money for trading")
            return False

        if self.position:  # if order exist
            print("order existed, cannot open buy order")  # error exist
            return False

        self.last_order_index = index   # record the index(excel row) during order made
        self.position = self.size
        print("Open buy order successed with close price " + str(self.df['Close'].iloc[index]))
        return True

    def sell(self, index):  # open sell order
        if self.cash_total < self.size * (self.df['Close'].iloc[index] + self.comission):  # check if the player has enough money
            print("Not enough money for trading")
            return False

        if self.position:  # if order exist
            print("order existed, cannot open buy order")  # error exist
            return False

        self.last_order_index = index   # record the index(excel row) during order made
        self.position = -self.size
        print("Open buy order successed with close price " + str(self.df['Close'].iloc[index]) + " on " + str(self.df['Datetime'].iloc[index]))
        return True

    def close(self, index):  # calculating profit during trade
        if self.position > 0:  # close buy order
            last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
            curr_price = self.df['Close'].iloc[index]  # get the close order price
            self.cash_total += self.position * (curr_price - last_price - self.comission * 2)  # calculation of buy profit
        elif self.position < 0:  # close sell order
            last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
            curr_price = self.df['Close'].iloc[index]  # get the close order price
            self.cash_total += self.position * (curr_price - last_price + self.comission * 2)  # calculation of sell profit
        self.position = 0           # change back to no order position
        print("Successed closing order with close price " + str(self.df['Close'].iloc[index]) + " on " + str(self.df['Datetime'].iloc[index]))

    def print_cash(self):
        print(f"Current asset : {self.cash_total}")
