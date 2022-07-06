import trade


class Player:

    def __init__(self, name: str, action: str):
        self.name = name              # name         :  the name of the player
        self.action = action          # action       :  buy/sell/close/no action
        self.__cash_total = 0

    def get__cash_total(self):  # the cash flow of the player
        return self.__cash_total

    def order_execute(self):  # the execution call for the trade
        pass
