
import neat
import os
import pickle
from indicators import Indicators
from player import Player
from utils import get_ks_deque

SYMBOL = 'EURUSD'


class Trade:
    def __init__(self, mode):
        self.indicators = Indicators(mode)
        self.df = self.indicators.get_df()
        self.traders = Player(self.df)

    def test_ai(self, net):
        pass

    def train_ai(self, genome, config, i):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """

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
    """
    Run each genome against eachother one time to determine the fitness.
    """

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        trade = Trade('train')
        trade.train_ai(genome, config, i)


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    trade = Trade()
    trade.test_ai(winner_net)


def start_train():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)


if __name__ == '__main__':
    for i in range(7):
        get_ks_deque(i,(2011,12,30,0,0,0),'EURUSD')
        start_train()
