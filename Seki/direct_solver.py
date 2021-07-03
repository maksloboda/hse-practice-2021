from numpy import sum

def is_board_final(field):
  return has_player_won(field, True) or has_player_won(field, False)

def has_player_won(field, is_r):
  axis = 1 if is_r else 0
  s = sum(field, axis=axis)
  return sum(s == 0) > 0

def _find_optimal_impl(field, is_r):
  """
  field - numpy matrix
  returns (x, y) of the optimal way, None incase of loss
  """
  copy = field.copy()
  for y in range(copy.shape[0]):
    for x in range(copy.shape[1]):
      if copy[y, x] == 0:
        continue
      copy[y, x] -= 1
      if is_board_final(copy):
        if has_player_won(copy, is_r):
          return (x, y)
        else:
          return None
      else:
        result = _find_optimal_impl(copy, not is_r)
        copy[y, x] += 1
        if result is None:
          return (x, y)
  return None

# Class used to iteratevly solve the game
class SekiSolver:
  def __init__(self, field) -> None:
      """
      Constructs the solver
      field - numpy matrix
      """
      self.field = field.copy()
  
  def decrement(self, x, y):
    """
    Decrements the field in the position x, y
    x - int
    y - int
    """
    self.field[y, x] -= 1

  def find_optimal(self, is_r):
    """
    Returns (x, y) of the the optimal decrement
    """
    return _find_optimal_impl(self.field, is_r)
