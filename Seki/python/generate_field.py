import numpy as np
import random
import os

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
    for i in range(number):
        with open(os.path.join(output_directory, str(i)), "w") as f:
            seki_field = generate_field(sum, n, m)
            f.write("{0} {1}\n".format(n, m))
            for i in range(m):
                for j in range(n):
                    f.write("{0} ".format(seki_field[i, j]))
                f.write("\n")

if __name__ == "__main__":
    num = int(input())
    sum = int(input())
    n = int(input())
    m = int(input())
    generate_samples(num, sum, n, m)
