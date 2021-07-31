#include "direct_solver.cpp"
#include <iostream>
#include <random>
#include <chrono>

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

  auto ss = SekiSolver(v, SekiType::SEKI);
  while (!ss.state.is_terminal()) {
    int x, y;
    cout << ss.state;
    cout << "x,y: ";
    cin >> x >> y;
    ss.decrement(x, y);
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    Move opt = ss.find_optimal(false);
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    double time_seconds = std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() / 1000000.0;
    cout << "time: " << time_seconds << "|matrices per second: " << ss.unrolled / time_seconds  <<  "|pr.value: " << opt.value << "|pr.x " << opt.x << "|pr.y " << opt.y << endl;
    ss.decrement(opt.x, opt.y);
  }

  cout << ss.state;

  return 0;
}