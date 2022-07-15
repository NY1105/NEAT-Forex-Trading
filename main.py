import datetime
import train_ai
import utils

train_ai.add_config()
today = (2012, 5, 12)
while True:
    utils.get_deque(today, 'train', 'EURUSD')
    train_ai.start_train()
    utils.update_date(today)
    if datetime.datetime(today[0], today[1], today[2]) > datetime.datetime(2022, 7, 14):
        break
