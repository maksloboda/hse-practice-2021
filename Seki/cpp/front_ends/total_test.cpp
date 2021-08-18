#include "core/core.h"
#include <iostream>
#include <random>
#include <chrono>

using namespace std;

int main() {
  srand(time(NULL));

  int is_seki, is_r;
  cin >> is_seki >> is_r;

  int n, m;
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

  auto ss = SekiSolver(v, is_seki ? SekiType::SEKI : SekiType::DSEKI, is_r);
  Move opt = ss.find_optimal();
  
  string outcome;

  if (opt.value == 0) {
    outcome = "D";
  } else if (opt.value < 0) {
    outcome = "R";
  } else {
    outcome = "C";
  }

  cout << outcome << endl;

  return 0;
}