import re
from core import Format
from core.board import Board, Square, Piece
from core.exceptions import NotBlankSpaceException, OverwritePositionException
from core.player import HumanPlayer, MachinePlayer


def str_format(s):
    return "{0:#^50}".format(s)

class Gomoku:
    def __init__(self, level):
        self.board = Board()
        self.p1 = self.select_player()
        self.p2 = HumanPlayer(self.board, Piece.WHITE, first=False)
        self.current_player = self.select_starter()
        self.print_board()
        self.level = level

    def select_player(self):
        print('Who would like to play?\n\n')

        while True:
            a = input('The Human Player (1)\nThe Machine Player (2)\nQuit (q)\n\n')

            if a == '1':
                return HumanPlayer(self.board, Piece.BLACK)
            if a == '2':
                print('Player 1 selected as The Machine!\n')
                return MachinePlayer(self.board, Piece.BLACK)
            if a == 'q':
                print('Bye Bye!')
                exit(0)

    def select_starter(self):
        a = input('Whom should start?\nPlayer (1) or Player (2)?\n')

        if a == '1':
            self.p2.first_move = True
            return self.p1
        self.p1.first_move = False
        return self.p2


    def print_board(self):
        print(self.board)
        print('\n')

    def run(self):
        while True:
            square = None
            if not isinstance(self.current_player, MachinePlayer):
                move = input(
                    Format.BOLD +
                    Format.Color.BLUE +
                    '[{}] '.format(self.current_player) + \
                    Format.END + \
                    'Enter with position [row,col] or "q" to quit game: ')
                print()

                if 'q' in move:
                    print(str_format(' Quit game '))
                    exit(0)

                row, col = re.findall('(\d+)', move)
                square = Square(int(row), int(col))
                last_index = len(self.board.table) - 1
                if (square.row > last_index) or (square.col > last_index):
                    print('Is permitted only row and col between 0 and {}\n\n'.format(last_index))
                    continue

            winner = Piece.NONE
            try:
                print(Format.Color.YELLOW + 'Wait move...\n' + Format.END)
                winner = self.current_player.play(square)
            except OverwritePositionException:
                print(Format.Color.RED + "Position not allowed!!\n\n" + Format.END)
                continue
            except NotBlankSpaceException:
                print(str_format(' There was no winner!!! '))
                exit(-1)

            self.print_board()
            current_play_str = Format.BOLD + \
                               Format.Color.GREEN + \
                               'Current Play: {}\n'.format(self.board.current_play) + \
                               Format.END
            print(current_play_str)

            if winner != Piece.NONE:
                print_winner = lambda s: print(Format.Color.BLUE + s + Format.END)
                print_winner(' Congratulations!!! ')
                print_winner(' {} is Winner! '.format(self.current_player))
                exit(0)

            self.current_player = self.p2 if self.current_player == self.p1 else self.p1
