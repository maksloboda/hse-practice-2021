from numpy import sum
from numpy.random import permutation as shuffle
import copy as cp


def is_field_terminal(field):
    return field.has_zero_row() or field.has_zero_col()


def eval_field_dseki(field, depth, is_r):
    if field.has_zero_row() and field.has_zero_col():
        return 0
    return eval_field_seki(field, depth, is_r)


def eval_field_seki(field, depth, is_r):
    """
    Gives a value for terminal position.
    R is minimizing while C is maximizing
    """
    assert (field.is_terminal())
    r_won = None

    if field.has_zero_row() and field.has_zero_col():
        r_won = not is_r
    elif field.has_zero_row():
        r_won = True
    else:
        r_won = False

    value = -1 if r_won else 1
    return value / depth


def from_matrix_to_number(F):  # преобразует матрицу в число
    number = ''
    for i in range(F.shape[0]):
        for j in range(F.shape[1]):
            if F[i][j] != 0:
                number += '1' * F[i][j]
                number += '0'
            else:
                number += '0'
    return int(number, base=2)


class Field:
    def __init__(self, data, row_sum=None, col_sum=None):
        self.data = data.copy()
        if row_sum is None:
            row_sum = sum(self.data, axis=1)
        if col_sum is None:
            col_sum = sum(self.data, axis=0)
        self.row_sum = row_sum.copy()
        self.col_sum = col_sum.copy()

    def add(self, x, y, v):
        self.data[y, x] += v
        self.row_sum[y] += v
        self.col_sum[x] += v

    def get(self, x, y):
        return self.data[y, x]

    def get_shape(self):
        return self.data.shape

    def has_zero_row(self):
        return min(self.row_sum) == 0

    def has_zero_col(self):
        return min(self.col_sum) == 0

    def is_terminal(self):
        return self.has_zero_row() or self.has_zero_col()

    def copy(self):
        return Field(self.data, self.row_sum, self.col_sum)

# Class containing data about the move
class Move:
    def __init__(self, value, x, y):
        # Guarantied value of the subtree
        self.value = value
        # Last move data
        self.x = x
        self.y = y

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value


def get_moves(field):
    if field.is_terminal():
        return
    copy = field.copy()
    shape = copy.get_shape()
    coords = [(y, x) for x in range(shape[1]) for y in range(shape[0])]
    coords = shuffle(coords)
    for y, x in coords:
        if copy.get(x, y) == 0:
            continue
        copy.add(x, y, -1)
        yield (copy, Move(0, x, y))
        copy.add(x, y, +1)


# Class used to iteratively solve the game
class SekiSolver:
    def __init__(self, matrix, type) -> None:
        """
        Constructs the solver
        matrix - numpy matrix
        type - string with value "seki" or "dseki"
        """
        self.field = Field(matrix)
        assert (type in ["seki", "dseki"])
        self.eval_field = eval_field_seki if type == "seki" else eval_field_dseki
        self.depth = 1
        self.unrolled = 0

    def decrement(self, x, y):
        """
        Decrements the field in the position x, y (zero based)
        x - int
        y - int
        """
        self.field.add(x, y, -1)
        self.depth += 1

    def _find_optimal_impl(self, field, depth, is_r, alpha, beta):
        """
        field - Field
        returns optimal move
        """
        # Try to evaluate the field right now
        if field.is_terminal():
            final_value = self.eval_field(field, depth, is_r)
            return Move(final_value, 0, 0)

        self.unrolled += 1

        # copy = field.copy()
        value = Move(2 if is_r else -2, 0, 0)
        for move in get_moves(field):
            m = move[0]
            new_value = self._find_optimal_impl(m, depth + 1, not is_r,
                                                alpha, beta)
            new_value.x = move[1].x
            new_value.y = move[1].y
            if is_r:
                value = cp.copy(min(value, new_value))
                if value <= alpha:
                    return value  # cut off
                beta = cp.copy(min(beta, value))
            else:
                value = cp.copy(max(value, new_value))
                if value >= beta:
                    return value  # cut off
                alpha = cp.copy(max(alpha, value))
        return value

    def find_optimal(self, is_r):
        """
        Returns optimal move
        """
        self.unrolled = 0
        v = self._find_optimal_impl(self.field, self.depth, is_r, Move(-2, 0, 0),
                                    Move(2, 0, 0))
        print(self.unrolled)
        return v
