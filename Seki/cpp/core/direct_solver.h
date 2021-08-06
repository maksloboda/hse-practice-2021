#ifndef DIRECT_SOLVER_H
#define DIRECT_SOLVER_H

#include <stdlib.h>
#include <vector>
#include <array>
#include <iostream>

constexpr size_t max_field_dim = 6;

class Move {
public:
  float value;
  int x, y;

  Move(float value, int x, int y);

  bool operator>(const Move &other) const;
  bool operator>=(const Move &other) const;
  bool operator<(const Move &other) const;
  bool operator<=(const Move &other) const;

};

class Field {
private:
  std::array<int, 2> shape;
  // [row][col]
  std::array<std::array<int, max_field_dim>, max_field_dim> data;
  std::array<int, max_field_dim> row_sum, col_sum;
public:
  Field(const std::vector<std::vector<int>> &new_data);

  void add(int x, int y, int v);

  int get(int x, int y) const;

  std::array<int, 2> get_shape() const;

  int get_min_row() const;
  int get_min_col() const;

  bool has_zero_row() const;
  bool has_zero_col() const;
  bool is_terminal() const;

  std::vector<Move> get_moves(bool is_reversed) const;

  friend std::ostream &operator<< (std::ostream &s, const Field &f);

};

enum SekiType {
  SEKI = 0,
  DSEKI,
};

typedef float (*eval_function_t)(const Field &, int, bool);

class SekiSolver {
public:
  Field state;
  int depth, unrolled;
  eval_function_t eval_function;

  SekiSolver(const std::vector<std::vector<int>> &matrix, SekiType type);

  void decrement(int x, int y);

  Move _find_optimal_impl(const Field &field, int depth, bool is_r,
      Move alpha, Move beta);

  Move find_optimal(bool is_r);

};

#endif // DIRECT_SOLVER_H
