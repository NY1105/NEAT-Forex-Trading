from player import Player
from indicators import Indicators
import time
import neat
import pickle
import os
import matplotlib
from tabulate import tabulate
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

class Trade:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.names = ['Hay', 'Leo']

    def test_ai(self, net):
        """
        Test the AI by passing a brain (Visualize case)
        """
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.right_paddle.y, abs(
                self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            self.game.draw(draw_score=True)
            pygame.display.update()

    def train_ai(self, genome1, genome2, config, draw=False):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        run = True
        cur_time = 0

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        max_hits = 50
        
        
        while run:

            game_info = self.game.loop()

            self.decision_to_actions(net1, net2, cur_time)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)

            pygame.display.update()

            duration = time.time() - start_time
            if game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                break
            cur_time += 1
        return False

    def decision_to_actions(self, net1, net2, time):
        """
        Determine where to move the left and the right paddle based on the two 
        neural networks that control them. <--- Decision to Actions
        """
        paddle = self.game.left_paddle#//
        
        genome = self.genome

        indicators = Indicators(time)

        p1 = Player(self.names[0], Indicators.get_df)
        p2 = Player(self.names[1], Indicators.get_df)

        players = [(self.genome1, net1, p1, True), (self.genome2, net2, p2, False)]

        for (genome, net, player, left) in players:

            output = net.activate((indicators.get_volume(), indicators.get_close_price(), indicators.get_SMA_diff()))
            decision = output.index(max(output))

            valid = True

            if decision == 0:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
            elif decision == 1:  # Move up
                p1.buy()
                valid = self.game.move_paddle(left=left, up=True)
            else:  # Move down
                valid = self.game.move_paddle(left=left, up=False)

            if not valid:  # If the movement makes the paddle go off the screen punish the AI
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
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


def test_best_network(config): #Run with best brain
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    pong = Trade(win, width, height)
    pong.test_ai(winner_net)

def start_pygame():
    pygame.init()
    surface = pygame.display.set_mode((1200, 400))
    color = (240, 255, 255)
    surface.fill(color)
    screen = pygame.display.get_surface()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    font = pygame.font.SysFont("monospace", 15)
    buy_label = font.render("Buy Order Opened at ", True, (0, 0, 0))
    sell_label = font.render("Sell Order Opened at ", True, (0, 0, 0))
    profit_label = font.render("Current profit: ", True, (0, 0, 0))
    screen.blit(buy_label, (800, 0))
    screen.blit(sell_label, (800, 50))
    screen.blit(profit_label, (800, 100))
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    start_pygame()
    run_neat(config)
    test_best_network(config)