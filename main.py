import player
import indicators
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pygame


def main():
    draw()


def draw():  # this plot the drawing of the period
    fig = plt.figure(figsize=(13, 5))
    price = indicators.df['Close']
    ax = fig.add_subplot()
    ax.set_ylabel('Price')
    ax.set_xlabel('Number Of Days')
    plt.plot(price)
    plt.show()


if __name__ == '__main__':
    main()
