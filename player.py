
class Player:

    def __init__(self, name: str, action: str):
        self.name = name              # name         :  the name of the player
        self.action = action          # action       :  buy/sell/close/no action
        self.__cash_total = 0

    def get__cash_total(self):
        return self.__cash_total
