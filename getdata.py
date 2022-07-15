from datetime import date
from fetch import *
from utils import daysinwhichmonth

SYMBOL = 'EURUSD'
PRICE_TYPES = ['BID']


for k in range(2010, 2023):  # year 2010-2022
    for i in range(1, 13):  # month
        end_day = daysinwhichmonth(i, k)
        fetch([SYMBOL], date(k, i, 1), date(k, i, end_day))
