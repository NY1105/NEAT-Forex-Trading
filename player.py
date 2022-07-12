class Player_Info:
    def __init__(self, cash_total, position):
        self.cash_total = cash_total
        self.position = position


class Player:

    def __init__(self, df):
        self.last_order_index = -1      # record     :  store the row of the trading in excel
        self.cash_total = 1000000       # cash total :  the initial cash amount of the player
        self.size = 100000              # lot size   :  for each lot the player invest with size of 10
        self.df = df                    # df         :  it is the dataframe
        self.position = 0               # position   :  -1 sell, 0 no order, 1 buy
        self.comission = 0.000035       # comission  :  comission in pip / size

    def buy(self, index):  # open buy order
        if self.cash_total < self.size * (self.df['Close'].iloc[index] + self.comission):
            # print("Not enough money for trading")
            return False

        if self.position:  # if order exist
            # print("order existed, cannot open buy order")  # error exist
            return False

        self.last_order_index = index   # record the index during order made
        self.position = self.size
        self.target_profit = self.df['Close'].iloc[index] * 1.005 #set target profit
        self.stop_loss = self.df['Close'].iloc[index] * 0.997 #set stop loss
        # print("Open buy order successed with close price " + str(self.df['Close'].iloc[index]) + " on " + str(self.df['Datetime'].iloc[index]) + " with total cash $" + str(self.cash_total))
        return True

    # def sell(self, index):  # open sell order
    #     if self.cash_total < self.size * (self.df['Close'].iloc[index] + self.comission):
    #         # print("Not enough money for trading")
    #         return False

    #     if self.position:  # if order exist
    #         # print("order existed, cannot open buy order")  # error exist
    #         return False

    #     self.last_order_index = index   # record the index during order made
    #     self.position = -self.size
    #     print("Open sell order successed with close price " + str(self.df['Close'].iloc[index]) + " on " + str(self.df['Datetime'].iloc[index]) + " with total cash $" + str(self.cash_total))
    #     return True

    # def close(self, index):  # calculating profit during trade
    #     profit = 0
    #     if self.position > 0:  # close buy order
    #         last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
    #         curr_price = self.df['Close'].iloc[index]  # get the close order price
    #         profit = self.position * (curr_price - last_price - self.comission * 2)  # calculation of buy profit
    #     elif self.position < 0:  # close sell order
    #         last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
    #         curr_price = self.df['Close'].iloc[index]  # get the close order price
    #         profit = self.position * (curr_price - last_price + self.comission * 2)  # calculation of sell profit

    #     self.cash_total += profit
    #     self.position = 0
    #     print("Successed closing order with close price " + str(self.df['Close'].iloc[index]) + " on " + str(self.df['Datetime'].iloc[index]) + ' and earning ' + str(profit) + ' with total earning $' + str(self.cash_total))

    #     return profit

    def check_close(self, index):  # TPSL close #check every bar
        last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
        curr_price = self.df['Close'].iloc[index]  # get the close order price
        profit = 0
        if curr_price >= self.target_profit or curr_price <= self.stop_loss: #if reached any target price
            profit = self.position * (curr_price - last_price - self.comission * 2)
            self.cash_total += profit
            self.position = 0
        if profit:
            print(profit)
        return profit

    def force_close(self, index):
        profit = 0
        last_price = self.df['Close'].iloc[self.last_order_index]  # get the open order price
        curr_price = self.df['Close'].iloc[index]  # get the close order price
        profit = self.position * (curr_price - last_price - self.comission * 2)
        self.cash_total += profit
        self.position = 0
        return profit

    def print_cash(self):
        print(f"Current asset : {self.cash_total}")

    def update(self):
        player_info = Player_Info(self.cash_total, self.position)
        return player_info
