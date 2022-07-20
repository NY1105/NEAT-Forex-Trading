from datetime import date
from fetch import *
from utils import daysinwhichmonth

SYMBOLS = [
    'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY',
    'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
    # 'EURUSD', 
    'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD',
    'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'
]
PRICE_TYPES = ['BID']


for k in range(2010, 2012):  # year 2010-2022
    for i in range(1, 13):  # month
        end_day = daysinwhichmonth(i, k)
        fetch(SYMBOLS, date(k, i, 1), date(k, i, end_day))
