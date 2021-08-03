
from direct_solver import SekiSolver
from direct_solver_with_get_moves import SekiSolver as SekiSolver_wgm
from numpy import array
import sys
import time
height, width = map(int, input("height, width:").split())

raw = []
print("input matrix:")
for i in range(height):
  arr = [*map(int, input().split())]
  if len(arr) != width:
    print("Row too long!", file=sys.stderr)
    sys.exit(1)
  raw.append(arr)

field = array(raw, dtype=int)
solver = SekiSolver(field, type="seki")

while True:
  print(solver.field.data)
  p = (*map(int, input("your move(x, y):").split()),)
  solver.decrement(*p)
  start = time.time() # start counting time
  pr = solver.find_optimal(False)
  end = time.time() # end counting time
  if pr is None:
    print("No optimal responce for C")
    break
  print('time:', end - start,'|matrices per second:', solver.unrolled/(end - start), '|pr.value:', pr.value, '|pr.x:', pr.x, '|pr.y:', pr.y)
  solver.decrement(pr.x, pr.y)
  if solver.field.is_terminal():
    print('game finished\n', solver.field.data)
    break

