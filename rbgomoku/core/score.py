import math

from core import Piece, utils

class ScoreEnum:
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


SCORE_POINT = [
    0,
    1,
    100,
    10000,
    1000000,
    50000000000
]

class Score:
    def __init__(self, table):
        self.score = 0
        self._table = table

    def has_winner(self, piece, board_space):
        """ Search for winner play in border

        :param piece: represent current piece played
        :param board_space: is a position played in matrix ex. BoardSpace(row, col)
        :return: the current winner if there or Piece.NONE if no there winner
        """
        if self._search_winner_diagonal(piece, board_space):
            """ Faz verificação da diagonal no sentido da diagonal principal
                se ocorrer uma vitória na diagonal atual
                escreve a peça ganhadora e retorna verdadeiro
            """
            return piece

        if self._search_winner_opp_diag(piece, board_space):
            """ Faz verificação da diagonal no sentido da diagonal secundária
                se ocorrer uma vitória na diagonal atual
                escreve a peça ganhadora e retorna verdadeiro
            """
            return piece

        if self._search_winner_line(piece, board_space):
            """ Faz verificação por linha
                se ocorrer uma vitória na linha atual
                escreve a peça ganhadora e retorna verdadeiro
            """
            return piece

        if self._search_winner_column(piece, board_space):
            """ Faz verificação por linha
                se ocorrer uma vitória na linha atual
                escreve a peça ganhadora e retorna verdadeiro
            """
            return piece

        return Piece.NONE

    def heuristic_move_score(self, piece, line):
        """ Calculate the current move

                 Calculate the score of current move in line list
                 This calc is done searching from maximum point until minimum point

        :param piece: current piece to calculate score
        :param line: list to calculate
        """
        score_factor = 1 if piece == Piece.BLACK else -1
        opponent = Piece.WHITE if piece == Piece.BLACK else Piece.BLACK
        line = ''.join(line)
        for i in range(ScoreEnum.FIVE, 0, -1):
            """ A generator to match sequence to search score
            """
            match = piece * i
            if match in line:
                bad_move = opponent + match + opponent
                if bad_move not in line:
                    self.score += (score_factor * SCORE_POINT[i])
                return

    def _search_winner_line(self, piece, board_space):
        """ Search has victory in line

                Check in matrix row if has match value to victory
                it get the previous five column position from current position played and
                the next five column position from current and check if has victory

        :param piece: current piece played
        :param board_space: is a position played in matrix ex. BoardSpace(row, col)
        :return: if has a victory in current line, True
                    otherwise is False
        """

        start_col = 0 if (board_space.col - ScoreEnum.FIVE) < 0 else (board_space.col - ScoreEnum.FIVE)
        size = len(self._table)
        end_col = size if (board_space.col + ScoreEnum.FIVE + 1) > size \
                            else (board_space.col + ScoreEnum.FIVE)


        sequence = self._table[board_space.row, start_col:end_col]
        self.heuristic_move_score(piece, sequence)
        return math.fabs(self.score) >= SCORE_POINT[ScoreEnum.FIVE]

    def _search_winner_column(self, piece, board_space):
        """ Search has victory in line

                Check in matrix column if has match value to victory
                it get the previous five row position from current position played and
                the next five row position from current and check if has victory

        :param piece: current piece played
        :param board_space: is a position played in matrix ex. BoardSpace(row, col)
        :return: if has a victory in current row, True
                    otherwise is False
        """
        start_row = 0 if (board_space.row - ScoreEnum.FIVE) < 0 else (board_space.row - ScoreEnum.FIVE)
        size = len(self._table)
        end_row = size if (board_space.row + ScoreEnum.FIVE + 1) > size \
                            else (board_space.row + ScoreEnum.FIVE)
        sequence = self._table[start_row:end_row, board_space.col]
        self.heuristic_move_score(piece, sequence)
        return math.fabs(self.score) >= SCORE_POINT[ScoreEnum.FIVE]

    def _search_winner_diagonal(self, piece, board_space):
        """ Search has victory by diagonal

                Check in matrix the diagonal if has match value to victory
                it get the previous five diagonal (row x col) position from current position played and
                the next five diagonal (row x col) position from current and check if has victory

        :param piece: current piece played
        :param board_space: is a position played in matrix ex. BoardSpace(row, col)
        :return: if has a victory in current diagonal, True
                    otherwise is False
        """
        offset = board_space.col - board_space.row
        diagonal = utils.get_diagonal(self._table, offset)

        if len(diagonal) < ScoreEnum.FIVE:
            return False

        self.heuristic_move_score(piece, diagonal)
        return math.fabs(self.score) >= SCORE_POINT[ScoreEnum.FIVE]

    def _search_winner_opp_diag(self, piece, board_space):
        """ Search has victory by diagonal

                Check in matrix the diagonal if has match value to victory
                it get the previous five diagonal (row x col) position from current position played and
                the next five diagonal (row x col) position from current and check if has victory

        :param piece: current piece played
        :param board_space: is a position played in matrix ex. BoardSpace(row, col)
        :return: if has a victory in current diagonal, True
                    otherwise is False
        """
        size = len(self._table)
        new_col = board_space.row
        new_row = (size - 1) - board_space.col
        offset = new_row - new_col
        opp_diagonal = utils.get_opposite_diagonal(self._table, offset)

        if len(opp_diagonal) < ScoreEnum.FIVE:
            return False

        self.heuristic_move_score(piece, opp_diagonal)
        return math.fabs(self.score) >= SCORE_POINT[ScoreEnum.FIVE]
