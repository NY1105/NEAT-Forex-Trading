import player
import indicators
import time
import neat
import pickle
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
fig = pylab.figure(figsize=[8, 4],  # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
ax = fig.gca()
ax.plot(indicators.df['Close'])
canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()
import pygame
from pygame.locals import *


class Trade:

    def __init__(self):
        pass

    def train_ai(self, genome, config, draw=False):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        run = True
        start_time = time.time()
        net1 = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome


def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i / len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = Trade(win, width, height)

            force_quit = pong.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):  # Run with best brain
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    Trade.test_ai(winner_net)

    # width, height = 700, 500
    # win = pygame.display.set_mode((width, height))
    # pygame.display.set_caption("Pong")
    # trade = Trade(width, height)


def main():
    pygame.init()
    surface = pygame.display.set_mode((1200, 400))
    color = (240, 255, 255)
    surface.fill(color)
    screen = pygame.display.get_surface()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    font = pygame.font.SysFont("monospace", 15)
    label = font.render("Data", True, (0, 0, 0))
    screen.blit(label, (800, 0))

    screen.blit(surf, (0, 0))
    pygame.display.flip()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True


if __name__ == '__main__':
    main()
    # config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    # config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    # run_neat(config)
    # test_best_network(config)
