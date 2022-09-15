from indicators import Indicators
from pathlib import Path
from player import Player
import datetime
import neat
import os
import os.path
import pickle
import utils
import visualize
import shutil


class Trade:
    def __init__(self, symbol='EURUSD', mode='train'):
        self.indicators = Indicators(symbol, mode)
        self.df = self.indicators.get_df()
        self.traders = Player(self.df)

    def test_ai(self, net, symbol='EURUSD'):
        utils.result_checkdir(symbol, 'test')
        index = 0
        while True:
            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position, False, symbol)
            if index == len(self.df) - 1:
                break
            index += 1
        print(self.traders.cash_total)
        visualize.visualise(self.traders.cash_total)

    def train_ai(self, genome, config, i, symbol='EURUSD'):
        # utils.result_checkdir(symbol, 'train')
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome
        index = 0
        while True:

            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position, True, symbol)

            if index == len(self.df) - 1:
                profit = self.traders.close(len(self.df) - 1)
                self.genome.fitness += profit
                if self.genome.fitness > 0:
                    print(f'Genome {i+1:02d}: {"%.2f" %self.genome.fitness}')
                else:
                    print(f'Genome {i+1:02d}: {"%.2f" %self.genome.fitness} {"X" * (1+(abs(int(self.genome.fitness))// 1000))}')
                break
            index += 1

    def decision_to_action(self, net, index, position, is_train, symbol='EURUSD'):
        price, volume, pricepct, volumepct = self.indicators.get_past_data(index, 15)
        mode = 'train'
        if not is_train:
            mode = 'test'
        if position > 0:
            position = 1
        elif position < 0:
            position = -1
        output = net.activate(tuple(pricepct[i] for i in range(15)) + tuple(volumepct[i] for i in range(15)) + (position, ))
        decision = output.index(max(output))

        if decision == 0:
            if self.traders.buy(index) and not is_train:
                print(f'Buy Price: {price[-1]}')
                with open(f'result/{symbol}_{mode}_result.csv', 'a') as f:
                    f.write(f'{self.df["Datetime"].iloc[index]},Buy,{price[-1]},0\n')

        elif decision == 1:
            if self.traders.sell(index) and not is_train:
                print(f'Sell Price: {price[-1]}')
                with open(f'result/{symbol}_{mode}_result.csv', 'a') as f:
                    f.write(f'{self.df["Datetime"].iloc[index]},Sell,{price[-1]},0\n')

        elif decision == 2:
            profit = self.traders.close(index)
            if is_train:
                self.genome.fitness += profit
                # with open(f'result/{symbol}_{mode}_result.csv', 'a') as f:
                #     f.write(f'{self.df["Datetime"].iloc[index]},Close,{price[-1]},{profit}\n')
            elif profit:
                print(f'Close Price: {price[-1]}, Profit: {profit}')
                with open(f'result/{symbol}_{mode}_result.csv', 'a') as f:
                    f.write(f'{self.df["Datetime"].iloc[index]},Close,{price[-1]},{profit}\n')


def eval_genomes(genomes, config, symbol='EURUSD'):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        trade = Trade(symbol, 'train')
        trade.train_ai(genome, config, i, symbol)
    # print(f'\nWin rate: {trade.win_count/i*100}%')


def run_neat(config_path):
    p = None
    # Restore checkpoint if checkpoint exists
    if os.path.exists('neat-checkpoint-4'):
        p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))  # overwrite checkpoint every 5 generations

    winner = p.run(eval_genomes, 5)

    with open("checkpoints/best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config, symbol='EURUSD'):
    with open("checkpoints/best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    trade = Trade(symbol, 'test')
    trade.test_ai(winner_net, symbol)


def init_train(symbol='EURUSD', today=(2010, 7, 1), end=(2010, 12, 31), train_days=30, train_hours=0, test_days=7, test_hours=0):
    today = tuple(datetime.date(*today[:3]).timetuple())[:6]
    if (datetime.date(*today[:3])).weekday() > 4:
        today = tuple((datetime.date(*today[:3]) + datetime.timedelta(days=7 - datetime.date(*today[:3]).weekday())).timetuple())[:6]
    if (datetime.date(*end[:3])).weekday() > 4:
        end = tuple((datetime.date(*end[:3]) + datetime.timedelta(days=7 - datetime.date(*end[:3]).weekday())).timetuple())[:6]
    utils.get_deque(now=end, mode='test', symbol=symbol, day=test_days, hour=test_hours)  # retrieve data for testing
    utils.get_deque(now=today, mode='train', symbol=symbol, day=train_days, hour=train_hours)  # fetch new csv to data/csv
    # add training config in the first training
    local_dir = Path(__file__).resolve().parent
    checkpoint_dir = local_dir / 'checkpoints'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    config_path = local_dir / 'config.txt'
    global config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         str(config_path))
    return train_days, train_hours, test_days, test_hours


def kickstart(symbol='EURUSD', today=(2010, 7, 5)):  # train with small period to large period
    if not os.path.exists('neat-checkpoint-4') or not os.path.exists('trained.txt'):
        shutil.rmtree('neat-checkpoint-4')
        with open('trained.txt', 'w') as f:
            f.write(f'{today[0]},{today[1]},{today[2]},{today[3]},{today[4]},{today[5]}')
    for i in range(7):
        print(utils.get_ks_deque(i, now=tuple(datetime(*today[0:6]).timetuple())[0:6], mode='train', symbol=symbol))
        run_neat(config)


def main(symbol='EURUSD', today=(2010, 7, 5), end=(2012, 12, 31), train_days=30, train_hours=0, test_days=7, test_hours=0):
    today = tuple(datetime.date(*today[:]).timetuple())[:6]
    end = tuple(datetime.date(end[0], end[1], end[2]).timetuple())[:6]
    # if os.path.exists('neat-checkpoint-4'):  # continue unfinished training
    if os.path.exists('trained.txt'):  # continue unfinished training
        with open('trained.txt') as f:
            line = f.readline()
        if line != '' and os.path.exists('neat-checkpoint-4'):
            date = line.split(',')
            today = (int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]),)
    while True:
        today = utils.update_datetime(today, shift_days=test_days, shift_hours=test_hours)  # update df before each training

        # break the training loop if arrived current date
        if datetime.datetime(*today[:6]) > datetime.datetime(*end[:6]):
            break
        utils.get_deque(now=today, mode='train', symbol=symbol, day=train_days, hour=train_hours)  # fetch new csv to data/csv

        run_neat(config)
        print(f'\n{today}')
        with open('trained.txt', 'w') as f:  # write the trained date to txt
            f.write(f'{today[0]},{today[1]},{today[2]},{today[3]},{today[4]},{today[5]}')


if __name__ == '__main__':
    today = (2011, 5, 24)
    end = (2011, 5, 30)
    symbol = 'EURUSD'
    train_days, train_hours, test_days, test_hours = 0, 24, 0, 6  # training and testing durations
    # recommended training to testing ratio is 4:1
    init_train(symbol, today, end, train_days=train_days, train_hours=train_hours, test_days=test_days, test_hours=test_hours)
    # kickstart(symbol, today) # training for smaller periods to larger periods
    main(symbol, today, end, train_days=train_days, train_hours=train_hours, test_days=test_days, test_hours=test_hours)
    test_best_network(config, symbol)
