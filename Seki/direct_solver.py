from numpy import sum
from numpy import np

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

  def decrement(self, x, y):
    """
    Decrements the field in the position x, y (zero based)
    x - int
    y - int
    """
    self.field[y, x] -= 1
    self.depth += 1

  def _find_optimal_impl(self, field, depth, is_r):
    """
    field - numpy matrix
    returns (x, y) of the optimal way, None incase of loss
    """
    v = 1 if is_r else -1
    v_pos = None
    copy = field.copy()
    for y in range(copy.shape[0]):
      for x in range(copy.shape[1]):
        if copy[y, x] == 0:
          continue
        copy[y, x] -= 1
        if is_field_terminal(copy):
          nv = self.eval_field(copy, depth, not is_r)
          v, v_pos = get_optimal(v, v_pos, nv, (x, y), is_r)
        else:
          result = self._find_optimal_impl(copy, depth + 1, not is_r)
          v, v_pos = get_optimal(v, v_pos, result[1], (x, y), is_r)
        copy[y, x] += 1
    return (v_pos, v)


  def find_optimal(self, is_r):
    """
    Returns (x, y) of the the optimal decrement
    """
    r = self._find_optimal_impl(self.field, self.depth, is_r)
    print(r[1])
    return r[0]

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
 print(from_matrix_to_number(np.array([[3, 0, 1], [1, 2, 3]])))
