import argparse

from view import console as c
from view.console import Gomoku

LEVEL = 2

def main():
    # parser = argparse.ArgumentParser(description='The RbGomoku game is console based.')
    # parser.add_argument('size_table',
    #                     metavar='N',
    #                     type=int,
    #                     help='table size NxN, MIN=3 and MAX=19')
    # args = parser.parse_args()

    print(c.str_format(' The RbGomoku game is console based. '))
    print()
    print(c.str_format(' Let\'s start '))
    print('\n\n')

    gomoku = Gomoku(LEVEL)
    gomoku.run()


if __name__ == '__main__':
    main()
