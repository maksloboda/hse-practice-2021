import numpy as np
import random
import os
import sys

def array_of_sum(cnt, s):
    indexes = np.arange(cnt)
    picked = random.choices(indexes, k=s)
    result = [0] * cnt
    for i in picked:
        result[i] += 1
    return result

def generate_field(sum, n, m):
    arr = np.array(array_of_sum(m * n, sum))
    seki_field = np.reshape(arr, (m, n))

    return seki_field

def generate_permutation(size):
    eye = np.eye(size)
    rng = np.random.default_rng()
    return rng.permutation(eye, axis=1)

def generate_complex_permutations(size, max_allowed_element, sum):
    if size * max_allowed_element < sum:
        #print("Impossible sum requested!", file=sys.stderr)
        return
    current = generate_permutation(size)
    while np.sum(current[0, :]) < sum:
        new = current + generate_permutation(size)
        if np.max(new) <= max_allowed_element:
            current = new
    return current

def setup_dir(path):
    if not path.endswith("_sf"):
        raise Exception(
            "Directory should end with '_sf' to be considered safe!")
    os.makedirs(path, exist_ok=True)
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if os.path.isfile(full_path):
            os.unlink(full_path)

def generate_samples(number, sum, n, m):
    output_directory = os.getenv("MATRIX_DIR", "test_matricies_sf")
    setup_dir(output_directory)
    for n in range(2, 7):
        for k in range(2, min(n * 2, int(20 / n) + 1)):
            for c in range(100):
                print(n, k, c)
                file_name = "{n}_{k}_{c}".format(n=n, k=k, c=c)
                with open(os.path.join(output_directory, file_name), "w") as f:
                    #print(f)
                    seki_field = generate_complex_permutations(n, 2, k).astype(int)
                    f.write("{0} {1}\n".format(n, n))
                    for i in range(n):
                        for j in range(n):
                            f.write("{0} ".format(seki_field[i, j]))
                        f.write("\n")

if __name__ == "__main__":
    #print(generate_complex_permutations(4, 2, 6))
    #exit()
    num = int(input())
    sum = int(input())
    n = int(input())
    m = int(input())
    generate_samples(num, sum, n, m)
