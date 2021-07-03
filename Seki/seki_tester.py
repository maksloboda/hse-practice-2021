from direct_solver import SekiSolver, has_player_won, is_board_final
from numpy import array
import sys

height, width = map(int, input("height, width:").split())

raw = []
for i in range(height):
  arr = [*map(int, input().split())]
  if len(arr) != width:
    print("Row too long!", file=sys.stderr)
    sys.exit(1)
  raw.append(arr)

field = array(raw, dtype=int)
solver = SekiSolver(field)

while True:
  print(solver.field)
  p = (*map(int, input("x, y").split()),)
  solver.decrement(*p)
  if has_player_won(solver.field, True):
    print("R won")
    break
  pr = solver.find_optimal(False)
  if pr is None:
    print("No optimal responce for C")
    break
  solver.decrement(*pr)
  if has_player_won(solver.field, False):
    print("C won")
    break
