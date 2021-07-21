#include "direct_solver.cpp"
#include <iostream>

int main() {
  Field f({{1, 2, 3}, {4, 5, 6}});
  cout << f.is_terminal() << endl;
  f.add(0, 0, -1);
  cout << f.is_terminal() << endl;
  f.add(0, 1, -4);
  cout << f.is_terminal() << endl;
  return 0;
}