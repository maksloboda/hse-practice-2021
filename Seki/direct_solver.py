from numpy import sum
from numpy.random import permutation as shuffle
import copy as cp

def has_zero_row(field):
  s = sum(field, axis=1)
  return sum(s == 0) > 0

def has_zero_col(field):
  s = sum(field, axis=0)
  return sum(s == 0) > 0

def is_field_terminal(field):
  return has_zero_row(field) or has_zero_col(field)

def eval_field_dseki(field, depth, is_r):
  if has_zero_row(field) and has_zero_col(field):
    return 0
  return eval_field_seki(field, depth, is_r)

def eval_field_seki(field, depth, is_r):
  """
  Gives a value for terminal position.
  R is minimizing while C is maximizing
  """
  assert(is_field_terminal(field))
  r_won = None

  if has_zero_row(field) and has_zero_col(field):
    r_won = not is_r
  elif has_zero_row(field):
    r_won = True
  else:
    r_won = False
  
  value = -1 if r_won else 1
  return value / depth

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
  if is_field_terminal(field):
    return
  copy = field.copy()
  coords = [(y, x) for x in range(copy.shape[1]) for y in range(copy.shape[0])]
  coords = shuffle(coords)
  for y, x in coords:
    if copy[y, x] == 0:
      continue
    copy[y, x] -= 1
    yield (copy, Move(0, x, y))
    copy[y, x] += 1

def get_optimal(current_value, current_pos, new_value, new_pos, is_r):
  if is_r:
    if current_value > new_value:
      return (new_value, new_pos)
    else:
      return (current_value, current_pos)
  else:
    if current_value < new_value:
      return (new_value, new_pos)
    else:
      return (current_value, current_pos)


# Class used to iteratevly solve the game
class SekiSolver:
  def __init__(self, field, type) -> None:
      """
      Constructs the solver
      field - numpy matrix
      type - string with value "seki" or "dseki"
      """
      self.field = field.copy()
      assert(type in ["seki", "dseki"])
      self.eval_field = eval_field_seki if type == "seki" else eval_field_dseki
      self.depth = 1
      self.unrolled = 0

  def decrement(self, x, y):
    """
    Decrements the field in the position x, y (zero based)
    x - int
    y - int
    """
    self.field[y, x] -= 1
    self.depth += 1

  def _find_optimal_impl(self, field, depth, is_r, alpha, beta):
    """
    field - numpy matrix
    returns optimal move
    """
    # Try to evaluate the field right now
    if is_field_terminal(field):
      final_value = self.eval_field(field, depth, is_r)
      return Move(final_value, 0, 0)
    
    self.unrolled += 1

    #copy = field.copy()
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
          return value # cut off
        beta = cp.copy(min(beta, value))
      else:
        value = cp.copy(max(value, new_value))
        if value >= beta:
          return value # cut off
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

  def from_matrix_to_number(F): #преобразует матрицу в число
    number = ''
    for i in range(F.shape[0]):
      for j in range(F.shape[1]):
        if F[i][j] != 0:
          number += '1' * F[i][j]
          number += '0'
        else:
          number += '0'
    return int(number, base = 2)
