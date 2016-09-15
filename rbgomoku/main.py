import argparse

from view import console as c
from view.console import Gomoku

BOARD_SIZE = 15


def main():
    # parser = argparse.ArgumentParser(description='The RbGomoku game is console based.')
    # parser.add_argument('size_table',
    #                     metavar='N',
    #                     type=int,
    #                     help='table size NxN, MIN=3 and MAX=19')
    # args = parser.parse_args()

    c.print_formatted(' The RbGomoku game is console based. ')
    c.print_formatted(' Let\'s start ')
    print('\n\n')

    gomoku = Gomoku(BOARD_SIZE)
    gomoku.run()



if __name__ == '__main__':
    main()