#!/bin/bash
for i in {1..100}
do
  echo "5 6" > matricies/$i
  python3 generate_field.py < generator_input >> matricies/$i
done