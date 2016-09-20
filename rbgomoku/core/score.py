import math
import re

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
        self.value = 0
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

    def heuristic(self, piece, line):
        """ Calculate the current move

                 Calculate the score of current move in line list
                 This calc is done searching from maximum point until minimum point

        :param piece: current piece to calculate score
        :param line: list to calculate
        """
        score_factor = 1 if piece == Piece.BLACK else -1

        for i in range(ScoreEnum.FIVE, 1, -1):
            """ A generator to match sequence to search score
            """
            line = ''.join(line)
            pattern = piece * i
            outmost = 0
            if pattern in line:
                match = re.search(pattern, line)
                if not match:
                    continue
                start, end = match.span()
                if (start > 0 and line[start - 1] == Piece.NONE):
                    outmost += 1
                if (end < len(line) and line[end] == Piece.NONE):  # end is the last position + 1
                    outmost += 1
                self.value += SCORE_POINT[i] * outmost * score_factor
                return self.value
            elif i == ScoreEnum.FOUR:
                pattern = '(x{3}\.x|x\.x{3})|(x{2}\.x{2})'
                match = re.search(pattern, line)
                if not match:
                    continue
                start, end = match.span()
                if (start > 0 and line[start - 1] == Piece.NONE):
                    outmost += 1
                if (end < len(line) and line[end] == Piece.NONE):  # end is the last position + 1
                    outmost += 1
                self.value += SCORE_POINT[i] * outmost * score_factor / 2
                return self.value
        return 1

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

        sequence = utils.get_line_by_position(self._table, board_space)
        value = self.heuristic(piece, sequence)
        return math.fabs(value) >= SCORE_POINT[ScoreEnum.FIVE]

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
        sequence = utils.get_column_by_position(self._table, board_space)
        value = self.heuristic(piece, sequence)
        return math.fabs(value) >= SCORE_POINT[ScoreEnum.FIVE]

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
        diagonal = utils.get_diagonal_by_position(self._table, board_space)

        if len(diagonal) < ScoreEnum.FIVE:
            return False

        value = self.heuristic(piece, diagonal)
        return math.fabs(value) >= SCORE_POINT[ScoreEnum.FIVE]

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
        opp_diagonal = utils.get_opp_diagonal_by_position(self._table, board_space)

        if len(opp_diagonal) < ScoreEnum.FIVE:
            return False

        value = self.heuristic(piece, opp_diagonal)
        return math.fabs(value) >= SCORE_POINT[ScoreEnum.FIVE]
