import player
from indicators import Indicators
import neat
import os


class Trader:
    def __init__(self):
        self.indicators = Indicators()
        self.df = self.indicators.get_df()
        self.trader = player.Player(self.df)

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome
        for day in range(len(self.df)):
            self.ai_move(net, day)

        self.calculate_fitness()

    def ai_move(self, net, day):
        output = net.activate((self.indicators.get_volume(day),
                               self.indicators.get_close(day),
                               self.indicators.get_ma_diff(day)))
        decision = output.index(max(output))
        if decision == 0:  # Don't move
            self.genome.fitness -= 0.5
        elif decision == 1:  # open buy
            self.trader.buy(day)
            self.genome.fitness += 0.1

        else:  # close order
            self.trader.close(day)
            self.genome.fitness += 0.1

    def calculate_fitness(self):
        self.genome.fitness += self.trader.cash_total
        # print(self.trader.cash_total)
        # print('complete')


def run_neat(config_path):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(eval_genomes, 5)


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        t = Trader()
        print(i)
        for _ in genomes[min(i + 1, len(genomes) - 1):]:
            t.train_ai(genome, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
