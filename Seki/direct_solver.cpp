#include <vector>
#include <array>
#include <numeric>
#include <algorithm>
#include <iostream>

using namespace std;

class Move {
public:
  float value;
  int x, y;

  Move(float value, int x, int y) {
    this->value = value;
    this->x = x;
    this->y = y;
  }

  bool operator>(const Move &other) const {
    return value > other.value;
  }

  bool operator>=(const Move &other) const {
    return value >= other.value;
  }

  bool operator<(const Move &other) const {
    return value < other.value;
  }

  bool operator<=(const Move &other) const {
    return value <= other.value;
  }

};

class Field {
private:
  array<int, 2> shape;
  // [row][col]
  vector<vector<int>> data;
  vector<int> row_sum, col_sum;
public:
  Field(const vector<vector<int>> &new_data) {
    data = new_data;
    int n_rows = new_data.size();
    int n_cols = new_data[0].size();
    shape[0] = n_rows;
    shape[1] = n_cols;
    row_sum.resize(n_rows);
    col_sum.resize(n_cols);
    for (int i = 0; i < n_rows; ++i) {
      row_sum[i] = accumulate(new_data[i].begin(), new_data[i].end(), 0);
    }
    for (int i = 0; i < n_cols; ++i) {
      col_sum[i] = 0;
      for (int j = 0; j < n_rows; ++j) {
        col_sum[i] += new_data[j][i];
      }
    }
  }

  void add(int x, int y, int v) {
    data[y][x] += v;
    row_sum[y] += v;
    col_sum[x] += v;
  }

  int get(int x, int y) const {
    return data[y][x];
  }

  array<int, 2> get_shape() const {
    return this->shape;
  }

  bool has_zero_row() const {
    auto it = min_element(row_sum.begin(), row_sum.end());
    return *it == 0;
  }

  bool has_zero_col() const {
    auto it = min_element(col_sum.begin(), col_sum.end());
    return *it == 0;
  }

  bool is_terminal() const {
    return this->has_zero_row() or this->has_zero_col();
  }

  vector<Move> get_moves() const {
    vector<Move> moves;

    for (int i = 0; i < shape[0]; ++i) {
      for (int j = 0; j < shape[1]; ++j) {
        if (data[i][j] != 0) {
          moves.emplace_back(0, j, i);
        }
      }
    }
    random_shuffle(moves.begin(), moves.end());
    return moves;
  }

  friend ostream &operator<< (ostream &s, const Field &f);

};

ostream &operator<< (ostream &s, const Field &f) {
  for (int i = 0; i < f.shape[0]; ++i) {
    for (int j = 0; j < f.shape[1]; ++j) {
      s << f.data[i][j] << " ";
    }
    s << "\n";
  }
  return s;
}

enum SekiType {
  SEKI = 0,
  DSEKI,
};

typedef float (*eval_function_t)(const Field &, int, bool);

float seki_eval_func(const Field &f, int depth, bool is_r) {
  bool r_won = false;
  if (f.has_zero_col() and f.has_zero_row()) {
    r_won = !is_r;
  } else if (f.has_zero_row()) {
    r_won = true;
  } else {
    r_won = false;
  }
  float value = r_won ? -1 : 1;
  return value / depth;
}

float dseki_eval_func(const Field &f, int depth, bool is_r) {
  if (f.has_zero_col() and f.has_zero_row()) {
    return 0;
  }
  return seki_eval_func(f, depth, is_r);
}

class SekiSolver {
public:
  Field state;
  int depth, unrolled;
  eval_function_t eval_function;

  SekiSolver(const vector<vector<int>> &matrix, SekiType type)
    : state(matrix) {
    depth = 1;
    unrolled = 0;
    switch (type)
    {
    case SekiType::SEKI:
      eval_function = seki_eval_func;
      break;
    case SekiType::DSEKI:
      eval_function = dseki_eval_func;
      break;
    default:
      throw new runtime_error("Invalid seki type");
      break;
    }
  }

  void decrement(int x, int y) {
    state.add(x, y, -1);
    ++depth;
  }

  Move _find_optimal_impl(const Field &field, int depth, bool is_r,
      Move alpha, Move beta) {
    if (field.is_terminal()) {
      float fv = eval_function(field, depth, is_r);
      return Move(fv, 0, 0);
    }

    unrolled += 1;
    auto value = Move(is_r ? 2 : -2, 0, 0);
    for (auto &m : field.get_moves()) {
      Field new_field = field;
      new_field.add(m.x, m.y, -1);
      Move new_value = _find_optimal_impl(new_field, depth + 1, !is_r,
          alpha, beta);
      new_value.x = m.x;
      new_value.y = m.y;
      if (is_r) {
        value = min(value, new_value);
        if (value <= alpha)
          return value;
        beta = min(beta, value);
      } else {
        value = max(value, new_value);
        if (value >= beta)
          return value;
        alpha = max(alpha, value);
      }
    }
    return value;
  }

  Move find_optimal(bool is_r) {
    unrolled = 0;
    Move opt = _find_optimal_impl(state, depth, is_r, Move(-2, 0, 0), Move(2, 0, 0));
    cerr << unrolled << endl;
    return opt;
  }

};
