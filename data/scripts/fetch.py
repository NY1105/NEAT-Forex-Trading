import os
from datetime import datetime, date, timedelta
import pathlib
from matplotlib.pyplot import bar
import requests
import lzma
import time
import random
import struct
import pandas as pd

SYMBOLS = ['USDJPY']
START_DATE = date(2022, 6, 20)
END_DATE = date(2022, 6, 24)
PERIODS = [0, 1, 5, 15, 30, 60, 240, 1440, 10080, 43200]
PATH = pathlib.PurePath(pathlib.Path('fetch.py').parent.absolute(), 'data', 'train')
PRICE_TYPES = ['BID']
SOURCE = 'Dukascopy'
##############################################################################################################

def date_xrange(start_date, end_date):
    # date generator
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def get_minute_bars_from_bi5_candlestick(date):
    for price_type in PRICE_TYPES:
        for symbol in SYMBOLS:
            year, month, day = date.isoformat().split('-')

            save_dir = os.path.join(PATH, symbol, year)
            save_filename = f'{month}_{day}.bi5'
            pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
            save_path = os.path.join(save_dir, save_filename)

            # try to get bi5 file from source

            # if not os.path.isfile(save_path):
            dukascopy_month = f'{int(month) - 1:02d}'  # Month in Dukascopy starts from 00 to 11
            time.sleep(random.uniform(1, 3))
            r = requests.get(f'https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{dukascopy_month}/{day}/{price_type}_candles_min_1.bi5')

            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)

            if os.path.isfile(save_path):
                period = 1  # minute bars are expected
                if 'JPY' in symbol:
                    pipette_to_price_ratio = 10 ** 3
                else:
                    pipette_to_price_ratio = 10 ** 5

                start_datetime = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
                with lzma.open(save_path, format=lzma.FORMAT_AUTO, filters=None) as f:
                    decompresseddata = f.read()

                df = pd.DataFrame(columns=['time','open','close','low','high','volume'])

                for i in range(int(len(decompresseddata) / 24)):
                    time_shift, open_price, close, low, high, volume = struct.unpack('!5if', decompresseddata[i * 24: (i + 1) * 24])
                    bar_time = start_datetime + timedelta(seconds=time_shift)
                    df.loc[len(df)] =  bar_time, open_price/ pipette_to_price_ratio, close/ pipette_to_price_ratio, low/ pipette_to_price_ratio, high/ pipette_to_price_ratio, volume
                    
                
                df.to_csv(PATH)

for date in date_xrange(START_DATE, END_DATE):
    get_minute_bars_from_bi5_candlestick(date)