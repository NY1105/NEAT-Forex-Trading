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

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

        index = 0
        while True:
            trader_info = self.traders.update()
            self.decision_to_action(net, index, trader_info.position)

            if index == len(self.df) - 1:
                profit = self.traders.close(len(self.df) - 1)
                self.genome.fitness += profit
                break
            index += 1

    def decision_to_action(self, net, index, position):
        price, volume = self.indicators.get_past_data(index,60)
        if position > 0:
            position = 1
        elif position < 0:
            position = -1
        output = net.activate((price[0],
                               price[1],
                               price[2],
                               price[3],
                               price[4],
                               price[5],
                               price[6],
                               price[7],
                               price[8],
                               price[9],
                               volume[0],
                               volume[1],
                               volume[2],
                               volume[3],
                               volume[4],
                               volume[5],
                               volume[6],
                               volume[7],
                               volume[8],
                               volume[9],
                               position
                               ))
        decision = output.index(max(output))

        if decision == 0:
            self.traders.buy(index)

        elif decision == 1:
            self.traders.sell(index)

        elif decision == 2:
            profit = self.traders.close(index)
            self.genome.fitness += profit


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        trade = Trade()
        trade.train_ai(genome, config)


def run_neat(config_path):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
