import generate_field as gf
import os
import subprocess
import numpy

max_matrix_dim = 6
max_sum = 22
retests = 20

def run_prog(is_seki, is_r, matrix):
  number_rows = matrix.shape[0]
  number_cols = matrix.shape[1]

  matrix_str = " ".join(
    map(lambda x: str(int(x)), [*matrix.flatten()])
  )

  inp = "{0} {1} {2} {3} {4}".format(is_seki, is_r, number_rows, number_cols,
      matrix_str)
  #print(inp)
  r = subprocess.run(["../cpp/bin/prog"], stdout=subprocess.PIPE,
    input=inp.encode("ascii"))
  result = r.stdout.decode("ascii").strip()
  return result


def check_prog(is_seki, is_r, matrix, expected):
  result = run_prog(is_seki, is_r, matrix)
  if (result != expected):
    raise Exception("Expected {expected}, got {actual} on {matrix}!".format(
      expected = expected, actual = result, matrix = matrix
    ))

failed_tests = 0

def run_test(func):
  def wrapped():
    global failed_tests
    try:
      func()
      print(func.__name__, "OK")
    except Exception as e:
      print(func.__name__, "failed!")
      print(str(e))
      failed_tests += 1
  return wrapped

@run_test
def test_1x1_seki():
  # One
  check_prog(1, 1, numpy.array([[1]]), "R")
  check_prog(1, 0, numpy.array([[1]]),"C")
  # Even
  check_prog(1, 1, numpy.array([[2]]), "C")
  check_prog(1, 1, numpy.array([[4]]), "C")
  check_prog(1, 1, numpy.array([[6]]), "C")
  check_prog(1, 0, numpy.array([[2]]), "R")
  check_prog(1, 0, numpy.array([[4]]), "R")
  check_prog(1, 0, numpy.array([[6]]), "R")
  # Odd
  check_prog(1, 0, numpy.array([[3]]), "C")
  check_prog(1, 0, numpy.array([[5]]), "C")
  check_prog(1, 0, numpy.array([[7]]), "C")
  check_prog(1, 1, numpy.array([[3]]), "R")
  check_prog(1, 1, numpy.array([[5]]), "R")
  check_prog(1, 1, numpy.array([[7]]), "R")

@run_test
def test_1x1_dseki():
  # One
  check_prog(0, 1, numpy.array([[1]]), "D")
  check_prog(0, 0, numpy.array([[1]]),"D")
  # Even
  check_prog(0, 1, numpy.array([[2]]), "D")
  check_prog(0, 1, numpy.array([[4]]), "D")
  check_prog(0, 1, numpy.array([[6]]), "D")
  check_prog(0, 0, numpy.array([[2]]), "D")
  check_prog(0, 0, numpy.array([[4]]), "D")
  check_prog(0, 0, numpy.array([[6]]), "D")
  # Odd
  check_prog(0, 0, numpy.array([[3]]), "D")
  check_prog(0, 0, numpy.array([[5]]), "D")
  check_prog(0, 0, numpy.array([[7]]), "D")
  check_prog(0, 1, numpy.array([[3]]), "D")
  check_prog(0, 1, numpy.array([[5]]), "D")
  check_prog(0, 1, numpy.array([[7]]), "D")

@run_test
def test_perm_seki():
  for sz in range(2, max_matrix_dim + 1):
    for _ in range(retests):
      for sum in range(2, sz * 2):
        mat = gf.generate_complex_permutations(sz, 2, sum)
        if mat is None or sum * sz > max_sum:
          break
        check_prog(1, 1, mat, "C")
        check_prog(1, 0, mat, "R")

@run_test
def test_one_perm_dseki():
  for _ in range(retests):
    for sz in range(2, max_matrix_dim + 1):
      for sum in range(2, sz):
        mat = gf.generate_complex_permutations(sz, 1, sum)
        if mat is None or sum * sz > max_sum:
          break
        check_prog(0, 1, mat, "C")
        check_prog(0, 0, mat, "R")

@run_test
def test_custom_seki():
  m1 = numpy.array([
    [0, 3, 3],
    [3, 3, 1],
    [3, 1, 2],
  ])
  check_prog(1, 0, m1, "R")
  check_prog(1, 1, m1, "C")

  m2 = numpy.array([
    [3, 2, 0],
    [2, 1, 3],
    [0, 3, 3],
  ])
  check_prog(1, 0, m2, "R")
  check_prog(1, 1, m2, "C")

  m3 = numpy.array([
    [0, 3, 3],
    [4, 0, 3],
    [4, 3, 0],
  ])
  check_prog(1, 0, m3, "C")
  check_prog(1, 1, m3, "C")

@run_test
def test_custom_dseki():
  m1 = numpy.array([
    [0, 3, 3],
    [3, 3, 1],
    [3, 1, 2],
  ])
  check_prog(0, 0, m1, "D")
  check_prog(0, 1, m1, "D")

  m2 = numpy.array([
    [3, 2, 0],
    [2, 1, 3],
    [0, 3, 3],
  ])
  check_prog(0, 0, m2, "D")
  check_prog(0, 1, m2, "D")

  m3 = numpy.array([
    [0, 3, 3],
    [4, 0, 3],
    [4, 3, 0],
  ])
  check_prog(0, 0, m3, "D")
  check_prog(0, 1, m3, "C")

def main():
  test_1x1_seki()
  test_1x1_dseki()
  test_custom_seki()
  test_custom_dseki()
  test_perm_seki()
  test_one_perm_dseki()

  if failed_tests:
    print(failed_tests, "failed!")
  else:
    print("All tests OK!")


if __name__ == "__main__":
  main()