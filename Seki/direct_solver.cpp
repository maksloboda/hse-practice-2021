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

  bool operator>(const Move &other) {
    return value > other.value;
  }

  bool operator>=(const Move &other) {
    return value >= other.value;
  }

  bool operator<(const Move &other) {
    return value < other.value;
  }

  bool operator<=(const Move &other) {
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

  vector<Move> get_moves() {
    vector<Move> moves;

    for (int i = 0; i < shape[0]; ++i) {
      for (int j = 0; j < shape[1]; ++j) {
        if (data[i][j] != 0) {
          moves.emplace_back(0, j, i);
        }
      }
    }
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
