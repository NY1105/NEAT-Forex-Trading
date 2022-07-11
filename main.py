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
            position = trader_info.position 
            output = net.activate((position,
                               self.indicators.get_trend(index)))
            decision = output.index(max(output))

            if position == 0:
                self.traders.buy(index)

            elif decision == 1:
                if position == 0:
                    self.traders.sell(index)

            elif decision == 2:

                if position != 0:
                    self.traders.close(index)

                if index == len(self.df) - 1:
                    self.traders.close(index)
                    self.calculate_fitness(trader_info.cash_total)
                    break
            index += 1
        print(self.traders.cash_total)

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
            if position == 0:
                self.traders.buy(index)

        elif decision == 1:
            if position == 0:
                self.traders.sell(index)

        elif decision == 2:

            if position != 0:
                self.genome.fitness += self.traders.close(index)

    def calculate_fitness(self, cash_total):
        self.genome.fitness += self.traders.close(len(self.df) - 1)
        print('complete')
        # print('fitness: ' + str(self.genome.fitness))


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

    winner = p.run(eval_genomes, 3)
    # with open("best.pickle", "wb") as f:
        # pickle.dump(winner, f)

def test_best_network(config):
    with open("best.pickle", "rb") as f:
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

    run_neat(config)
