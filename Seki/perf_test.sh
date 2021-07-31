#!/bin/bash
echo "time, unrolled, speed, value, x, y" > perf_res
for i in {1..100}
do
  ./perf < matricies/$i >> perf_res
done