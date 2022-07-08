import csv
from datetime import datetime, date, timedelta
from lib2to3.pygram import Symbols
from operator import index
from pathlib import Path
import concurrent.futures
import lzma
import pandas as pd
import random
import requests
import struct
import time
import os

# default date range
START_DATE = date(2022, 6, 13)
END_DATE = date(2022, 6, 17)

# default parameters for data source
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ROOT = PROJECT_ROOT / 'data' 
DATA_ROOT.mkdir(parents=True, exist_ok=True)

CSV_ROOT = PROJECT_ROOT / 'data' / 'csv'
CSV_ROOT.mkdir(parents=True, exist_ok=True)


SYMBOLS = ['EURUSD']
PRICE_TYPES = ['BID']

NUMBER_OF_WORKERS = 4


def date_xrange(start_date, end_date):
    # date generator
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


def get_minute_bars_from_bi5_candlestick(date):
    for price_type in PRICE_TYPES:
        for symbol in SYMBOLS:
            year, month, day = date.isoformat().split('-')

            save_root = DATA_ROOT / 'dukascopy' / f'{symbol}' / f'{price_type}'
            save_root.mkdir(parents=True, exist_ok=True)

            save_path = save_root / f'{month}_{day}.bi5'

            # try to get bi5 file from source

            # if not os.path.isfile(save_path):
            dukascopy_month = f'{int(month) - 1:02d}'  # Month in Dukascopy starts from 00 to 11
            time.sleep(random.uniform(1, 3))
            r = requests.get(f'https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{dukascopy_month}/{day}/{price_type}_candles_min_1.bi5')

            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)

            if os.path.isfile(save_path):
                
                if 'JPY' in symbol:
                    pipette_to_price_ratio = 10 ** 3
                else:
                    pipette_to_price_ratio = 10 ** 5

                start_datetime = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
                with lzma.open(save_path, format=lzma.FORMAT_AUTO, filters=None) as f:
                    decompresseddata = f.read()

                df = []
                indextime = []
                for i in range(int(len(decompresseddata) / 24)):
                    time_shift, open_price, close, low, high, volume = struct.unpack('!5if', decompresseddata[i * 24: (i + 1) * 24])

                    bar_time = start_datetime + timedelta(seconds=time_shift)
                    open_price /= pipette_to_price_ratio
                    high /= pipette_to_price_ratio
                    low /= pipette_to_price_ratio
                    close /= pipette_to_price_ratio
                    volume *= 10 ** 7

                    indextime.append(bar_time)
                    df.append([open_price, high, low, close, volume])

                df = pd.DataFrame(data=df, index=indextime, columns=['Open', 'High', 'Low', 'Close', 'Volume'])
                
            csv_path = CSV_ROOT / f'{symbol}.csv'

            if not os.path.isfile(csv_path):
                with open(csv_path, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(['Datetime','Open', 'High', 'Low', 'Close', 'Volume'])

            df.to_csv(csv_path, mode='a', header=False)
            break


if __name__ == '__main__':
    # collect all paths of bi5 files
    # with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
    #     future_to_path = {executor.submit(get_minute_bars_from_bi5_candlestick, date): date for date in date_xrange(START_DATE, END_DATE)}
    #     for future in concurrent.futures.as_completed(future_to_path):
    #         pass
    for symbol in SYMBOLS:
        csv_path = CSV_ROOT / f'{symbol}.csv'
        if os.path.isfile(csv_path):
            os.remove(csv_path)

    for date in date_xrange(START_DATE, END_DATE):
        get_minute_bars_from_bi5_candlestick(date)
