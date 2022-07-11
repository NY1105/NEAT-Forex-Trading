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
                self.traders.close(index)
                self.calculate_fitness(trader_info.cash_total)
                break
            index += 1

    def decision_to_action(self, net, index, position):

        output = net.activate((position,
                               self.indicators.get_trend(index)))
        decision = output.index(max(output))

        if decision == 0:
            self.genome.fitness -= 1

        elif decision == 1:
            if position == 0:
                self.traders.buy(index)
                self.genome.fitness += 4
            else:
                self.genome.fitness -= 4

        elif decision == 2:
            if position == 0:
                self.traders.sell(index)
                self.genome.fitness += 4
            else:
                self.genome.fitness -= 4
        else:
            if position != 0:
                self.traders.close(index)
                self.genome.fitness += 4
            else:
                self.genome.fitness -= 4

    def calculate_fitness(self, cash_total):
        self.genome.fitness += cash_total
        print('cash total: ' + str(cash_total))
        print('fitness: ' + str(self.genome.fitness))


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

    winner = p.run(eval_genomes, 5)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
