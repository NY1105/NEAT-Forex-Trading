import player
import indicators


def main():
    p1 = player.Player("Leo", indicators.df)
    p1.print_cash()
    p1.sell(0)
    p1.close(1)
    p1.print_cash()


if __name__ == '__main__':
    main()
