import player
from indicators import Indicators
import neat
import os


class Trader:
    def __init__(self):
        self.indicators = Indicators()  # get the indicator object
        self.df = self.indicators.get_df()  # get the dataframe
        self.trader = player.Player(self.df)  # set the trader

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # create the neat network
        self.genome = genome
        for day in range(len(self.df)):
            self.ai_move(net, day)

        self.calculate_fitness()

    def ai_move(self, net, day):
        output = net.activate((self.indicators.get_volume(day),
                               self.indicators.get_close(day),
                               self.indicators.get_sma_diff_pct(day),
                               self.indicators.get_price_diff_with_prev(day),
                               self.indicators.get_trend(day),
                               self.indicators.get_rsi(day)
                               ))
        decision = output.index(max(output))
        # print(decision)
        if decision == 0:  # Don't move
            # self.genome.fitness -= 0.02
            self.genome.fitness *= 0.98
        elif decision == 1:  # open buy
            self.trader.buy(day)
            # self.genome.fitness += 0.01
            self.genome.fitness *= 1.01
        elif decision == 2:  # sell buy
            self.trader.sell(day)
            # self.genome.fitness += 0.01
            self.genome.fitness *= 1.01
        elif decision == 3:  # close order
            self.trader.close(day)
            # self.genome.fitness += 0.01
            self.genome.fitness *= 1.01

    def calculate_fitness(self):
        self.genome.fitness += self.trader.cash_total
        # print(self.genome.fitness)


def run_neat(config_path):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(eval_genomes, 500)


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        t = Trader()
        genome.fitness = 0
        t.train_ai(genome, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
