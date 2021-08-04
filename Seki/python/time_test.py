#!/bin/python3
import os
import subprocess
from typing import Text

input_directory = os.getenv("INPUT_DIR", "test_matricies")

res = open("perf_result.csv", "w")

res.write("index, time, unrolled, speed, value, x, y" + "\n")

for file_name in os.listdir(input_directory):
  with open(os.path.join(input_directory, file_name)) as f:
    r = subprocess.run(["../cpp/bin/prog"], capture_output=True, text=True,
      stdin=f)
    res.write("{0},".format(file_name))
    res.write(r.stdout)

res.close()