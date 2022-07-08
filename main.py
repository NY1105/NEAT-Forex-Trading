from numpy import outer
import player
import indicators
import neat
import os


def eval_genomes(genomes, config):
    global ge, nets, points, player_list
    points = 0                               # this is the point of the ai
    ge = []                                  # this store each generation in the list
    nets = []                                # this put the generation into the neat trading
    player_list = []                         # this store a list of player
    for genome in genomes:
        player_list.append(player.Player())  # put the Broker to broker list
        ge.append(genome)                    # add the geneme to the neat
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)                     # add to the generation
        genome.fitness = 0                   # init the fitness as 0

    if len(player_list) == 0:                # check if the list empty
        return

    for index, player_in_list in enumerate(player_list):
        output = nets[index].activate()


def run(config_path):
    global pop
    config = neat.config.Config(  # this config the neat file
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)   # this put the generation to the neat population
    pop.run(eval_genomes, 50)       # run 50 generation


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
