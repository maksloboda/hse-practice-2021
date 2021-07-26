import numpy as np
import random
import math

def matrix_of_sum(cnt, s):
    if cnt == 1:
        return [s]
    num = random.randint(0, s // cnt)
    return [num] + matrix_of_sum(cnt - 1, s - num)

def generate_field():
    print("type in value for s")
    s = int(input())
    while s <= 0:
        print("unsuitablle value for S")
        print("try again")
        s = int(input())
    print("insert 1 if you want to have cols/rows with sum = 1 or 0 otherwise")
    sum1 = int(input())
    while sum1 != 0 and sum1 != 1:
        print("try again")
        sum1 = int(input())
    print("insert 1 if you want to choose values for m and n or 0 otherwise")
    insert = int(input())
    while insert != 0 and insert != 1:
        print("try again")
        insert = int(input())
    if insert == 0:
        m = random.randint(2, min(math.ceil(math.sqrt(s)), 25))
        n = random.randint(2, min(math.ceil(math.sqrt(s)), 25))
    else:
        print("insert m")
        m = int(input())
        if m < 2:
            print("unsuitablle value for m")
            print("try again")
            m = int(input())
        print("insert n")
        n = int(input())
        if n < 2:
            print("unsuitablle value for n")
            print("try again")
            n = int(input())
    print("matrix size is ", end="")
    print(m, end="")
    print(" x ", end="")
    print(n)

    seki_field = np.zeros((m, n))
    if sum1 == 1:
        while (~seki_field.any(axis=0)).any() or (~seki_field.any(axis=1)).any():
            arr = np.array(matrix_of_sum(m * n, s))
            seki_field = np.reshape(arr, (m, n))
            np.random.shuffle(seki_field)
    else:
        while (seki_field.sum(axis=0) < 2).any() or (seki_field.sum(axis=0) < 2).any():
            arr = np.array(matrix_of_sum(m * n, s))
            seki_field = np.reshape(arr, (m, n))
            np.random.shuffle(seki_field)
        
    print(seki_field)
