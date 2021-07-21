#include "direct_solver.cpp"
#include <iostream>
#include <random>

int main() {
  srand(time(NULL));
  Field f({{0, 2, 3}, {4, 0, 6}});
  cout << f << endl;
  vector<Move> moves = f.get_moves();
  for (auto &m : moves) {
    cout << m.x << " " << m.y << endl;
  }
  return 0;
}