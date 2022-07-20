import datetime
import gzip
import os
import random
from turtle import update
import neat
import pickle

from indicators import Indicators
from player import Player
import os.path
from pathlib import Path
import utils
import visualize

SYMBOL = 'EURUSD'


class Trade:
    def __init__(self, mode):
        self.indicators = Indicators(mode)
        self.df = self.indicators.get_df()
        self.traders = Player(self.df)

    def test_ai(self, net):
        utils.result_checkdir(SYMBOL)
        index = 0
        # self.f = open(f'{SYMBOL}_result.csv', "a")
        while True:
            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position, False)
            if index == len(self.df) - 1:
                break
            index += 1
        # self.f.close()
        print(self.traders.cash_total)
        visualize.visualise()

    def train_ai(self, genome, config, i):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

        index = 0
        while True:
            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position, True)
            if index == len(self.df) - 1:
                profit = self.traders.close(len(self.df) - 1)
                self.genome.fitness += profit
                print(f'Genome {i+1}: {"%.2f" %self.genome.fitness}')
                break
            index += 1

    def decision_to_action(self, net, index, position, is_train):
        price, volume, pricepct, volumepct = self.indicators.get_past_data(index, 15)

        if position > 0:
            position = 1
        elif position < 0:
            position = -1
        output = net.activate((pricepct[0], pricepct[1], pricepct[2], pricepct[3], pricepct[4], pricepct[5], pricepct[6], pricepct[7], pricepct[8], pricepct[9], pricepct[10], pricepct[11], pricepct[12], pricepct[13], pricepct[14], volumepct[0], volumepct[1], volumepct[2], volumepct[3], volumepct[4], volumepct[5], volumepct[6], volumepct[7], volumepct[8], volumepct[9], volumepct[10], volumepct[11], volumepct[12], volumepct[13], volumepct[14], position))
        decision = output.index(max(output))

        if decision == 0:
            if self.traders.buy(index) and not is_train:
                print(f'Buy Price: {price[-1]}')
                with open(f'result/{SYMBOL}_result.csv', "a") as f:
                    f.write(f'{self.df["Unnamed: 0"].iloc[index]},Buy,{price[-1]},0\n')

        elif decision == 1:
            if self.traders.sell(index) and not is_train:
                print(f'Sell Price: {price[-1]}')
                with open(f'result/{SYMBOL}_result.csv', "a") as f:
                    f.write(f'{self.df["Unnamed: 0"].iloc[index]},Sell,{price[-1]},0\n')

        elif decision == 2:
            profit = self.traders.close(index)
            if is_train:
                self.genome.fitness += profit
            elif profit:
                print(f'Close Price: {price[-1]}, Profit: {profit}')
                with open(f'result/{SYMBOL}_result.csv', "a") as f:
                    f.write(f'{self.df["Unnamed: 0"].iloc[index]},Close,{price[-1]},{profit}\n')


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        trade = Trade('train')
        trade.train_ai(genome, config, i)


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


def test_best_network(config):
    with open("checkpoints/best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    trade = Trade('test')
    trade.test_ai(winner_net)


def init_train():
    # add training config in the first training
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    global config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)


if __name__ == '__main__':
    today = (2010, 3, 1)
    if os.path.exists('neat-checkpoint-4'):
        with open('trained.txt') as f:
            line = f.readline()
        date = line.split(',')
        today = (int(date[0]), int(date[1]), int(date[2]))
    init_train()
    while True:
        today = utils.update_date(today)  # update df before each training

        # break the training loop if arrived current date
        if datetime.datetime(today[0], today[1], today[2]) > datetime.datetime(2011, 5, 30):
            break

        utils.get_deque(today, 'train', 'EURUSD')  # fetch new csv to data/csv

        run_neat(config)

        with open('trained.txt', 'w') as f:  # write the trained date to txt
            f.write(f'{today[0]},{today[1]},{today[2]}')
    test_best_network(config)
