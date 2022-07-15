from main import main
from utils import get_deque

train()
while True:
    today = (2012, 5, 12)
    get_deque(today, 'train')
    get_deque(today, 'test')
    train()
    trade()