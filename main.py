from cgi import test
import os
import neat
import pickle

from indicators import Indicators
from player import Player


class Trade:
    def __init__(self):
        self.indicators = Indicators()
        self.df = self.indicators.get_df()
        self.traders = Player(self.df)

    def test_ai(self, net):
        index = 0
        while True:
            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position, False)
            if index == len(self.df) - 1:
                break
            index += 1
        print(self.traders.cash_total)

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
        price, volume = self.indicators.get_past_data(index, 30)
        if position > 0:
            position = 1
        elif position < 0:
            position = -1
        output = net.activate((price[0], price[1], price[2], price[3], price[4], price[5], price[6], price[7], price[8], price[9], price[10], price[11], price[12], price[13], price[14], price[15], price[16], price[17], price[18], price[19], price[20], price[21], price[22], price[23], price[24], price[25], price[26], price[27], price[28], price[29], volume[0], volume[1], volume[2], volume[3], volume[4], volume[5], volume[6], volume[7], volume[8], volume[9], volume[10], volume[11], volume[12], volume[13], volume[14], volume[15], volume[16], volume[17], volume[18], volume[19], volume[20], volume[21], volume[22], volume[23], volume[24], volume[25], volume[26], volume[27], volume[28], volume[29], position))
        decision = output.index(max(output))

        if decision == 0:
            record = self.traders.buy(index)
            if record and not is_train:
                print(f'Buy Price: {price[-1]}')

        elif decision == 1:
            record = self.traders.sell(index)
            if record and not is_train:
                print(f'Sell Price: {price[-1]}')

        elif decision == 2:
            profit = self.traders.close(index)
            if is_train:
                self.genome.fitness += profit
            else:
                print(f'Close Price: {price[-1]}')


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        trade = Trade()
        trade.train_ai(genome, config, i)


def run_neat(config_path):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 20)

    # checkpoint_root = 'checkpoints/'
    # checkpoint_root.mkdir(parents=True, exist_ok=True)
    with open("checkpoints/best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("checkpoints/best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    trade = Trade()
    trade.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # run_neat(config)
    test_best_network(config)
