import numpy as np

MAJOR_SEQUENCE = 5


def get_diagonal(table, offset):
    """ Get diagonal from table

                Get a list elements referencing the diagonal by offset from main diagonal

        :param table: matrix to get diagonal
        :param offset: Offset of the diagonal from the main diagonal.
                       Can be positive or negative. Defaults to main diagonal (0).
        :return: list elements from request diagonal
    """
    diagonal = np.diag(table, k=offset).tolist()
    return diagonal


def get_opposite_diagonal(table, offset):
    """ Get diagonal from table

                Get a list elements referencing the opposite
                diagonal by offset from opposite diagonal
                Positive get below, and negative get higher diagonal from opposite diagonal
                   0  1  2  3  4
                0  a  a  a  a  .
                1  a  a  a  .  b
                2  a  a  .  b  b
                3  a  .  b  b  b
                4  .  b  b  b  b

        :param table: matrix to get diagonal
        :param offset: Offset of the opposite diagonal from the main diagonal.
                       Can be positive or negative. Defaults to opposite diagonal (0).
        :return: list elements from request opposite diagonal
    """
    column_inverted = table[:, ::-1]
    transposed = column_inverted.transpose()
    inverted_opp_diagonal = np.diag(transposed, k=-offset).tolist()
    opposite_diagonal = inverted_opp_diagonal[::-1]
    return opposite_diagonal


def get_diagonal_by_position(table, board_space):
    offset = board_space.col - board_space.row
    return get_diagonal(table, offset)

def get_line_by_position(table, board_space):
        start_col = 0 if (board_space.col - MAJOR_SEQUENCE) < 0 else (board_space.col - MAJOR_SEQUENCE)
        size = len(table)
        end_col = size if (board_space.col + MAJOR_SEQUENCE + 1) > size \
            else (board_space.col + MAJOR_SEQUENCE)
        return table[board_space.row, start_col:end_col]

def get_column_by_position(table, board_space):
    start_row = 0 if (board_space.row - MAJOR_SEQUENCE) < 0 else (board_space.row - MAJOR_SEQUENCE)
    size = len(table)
    end_row = size if (board_space.row + MAJOR_SEQUENCE + 1) > size \
        else (board_space.row + MAJOR_SEQUENCE)
    return table[start_row:end_row, board_space.col]

def get_opp_diagonal_by_position(table, board_space):
        size = len(table)
        new_col = board_space.row
        new_row = (size - 1) - board_space.col
        offset = new_row - new_col
        return get_opposite_diagonal(table, offset)