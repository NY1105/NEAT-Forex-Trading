import os

symbol = 'USDJPY'
date = '2022-06-22'
os.system('duka '+ symbol +' -d '+ date +' -c M1 -f data/train --header')