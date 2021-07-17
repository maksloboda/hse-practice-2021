from direct_solver import SekiSolver
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
solver = SekiSolver(field, type="seki")

while True:
  print(solver.field.data)
  p = (*map(int, input("x, y").split()),)
  solver.decrement(*p)
  pr = solver.find_optimal(False)
  if pr is None:
    print("No optimal responce for C")
    break
  print(pr.value, pr.x, pr.y)
  solver.decrement(pr.x, pr.y)
