#include "core/core.h"
#include <iostream>
#include <random>
#include <chrono>

using namespace std;

int main() {
  srand(time(NULL));
  int n, m;
  cout << "height, width\n";
  cin >> n >> m;
  vector<vector<int>> v;
  for (int i = 0; i < n; ++i) {
    v.push_back(vector<int>());
    for (int j = 0; j < m; ++j) {
      int f;
      cin >> f;
      v.back().push_back(f);
    }
  }

  auto ss = SekiSolver(v, SekiType::SEKI, PassType::ANY_PASS, false);
  while (!ss.get_state().is_terminal()) {
    int x, y;
    cout << ss.get_state().get_field();
    cout << "x,y: ";
    cin >> x >> y;
    Move m = Move(0.0, x, y);
    if (x < 0) {
      m.is_pass = true;
    }
    ss.apply_move(m);
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    Move opt = ss.find_optimal();
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    double time_seconds = std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000000.0;
    cout << "time: " << time_seconds << "|matrices per second: " << ss.unrolled / time_seconds  <<  "|pr.value: " << opt.value << "|pr.x " << opt.x << "|pr.y " << opt.y << endl;
    ss.apply_move(opt);
  }
  
  cout << ss.get_state().get_field();
  
  return 0;
}