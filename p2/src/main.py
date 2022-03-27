import random
import time
from copy import copy
from tracemalloc import start
import numpy as np
import matplotlib.pyplot as plt


"we received the best results with such value"
L = 2**4
global flop_counter


def mul(A, B, C, ax, ay, bx, by, cx, cy, n):
    global flop_counter
    if n <= L:
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    C[cx + a][cy + b] += A[ax + a][ay + c] * B[bx + c][by + b]
                    flop_counter = flop_counter + 2
    else:
        h = int(n/2)
        mul(A, B, C, ax, ay, bx, by, cx, cy, h)
        mul(A, B, C, ax, ay + h, bx + h, by, cx, cy, h)
        mul(A, B, C, ax, ay, bx, by + h, cx, cy + h, h)
        mul(A, B, C, ax, ay + h, bx+h, by+h, cx, cy+h, h)
        mul(A, B, C, ax+h, ay, bx, by, cx+h, cy, h)
        mul(A, B, C, ax+h, ay+h, bx+h, by, cx+h, cy, h)
        mul(A, B, C, ax+h, ay, bx, by+h, cx+h, cy+h, h)
        mul(A, B, C, ax+h, ay+h, bx+h, by+h, cx+h, cy+h, h)


def inverse(A):
    global flop_counter
    n = len(A)
    if n == 1:
        if A[0][0] == 0:
            return [[0]]
        return [[1/A[0][0]]]
    h = int(n/2)
    A11 = copy([row[:h] for row in A[:h]])
    A12 = copy([row[h:] for row in A[:h]])
    A21 = copy([row[:h] for row in A[h:]])
    A22 = copy([row[h:] for row in A[h:]])

    A11_inverse = inverse(A11)
    A11_inverse_A12 = [[0 for _ in range(h)] for _ in range(h)]
    mul(A11_inverse, A12, A11_inverse_A12, 0, 0, 0, 0, 0, 0, h)
    A21_A11_inverse_A12 = [[0 for _ in range(h)] for _ in range(h)]
    mul(A21, A11_inverse_A12, A21_A11_inverse_A12, 0, 0, 0, 0, 0, 0, h)
    S22 = [[A22[i][j] - A21_A11_inverse_A12[i][j] for j in range(h)] for i in range(h)]
    flop_counter = flop_counter + (h**2)

    S22_inverse = inverse(S22)
    A21_A11_inverse = [[0 for _ in range(h)] for _ in range(h)]
    mul(A21, A11_inverse, A21_A11_inverse, 0, 0, 0, 0, 0, 0, h)

    A11_inverse_A12_S22_inverse = [[0 for _ in range(h)] for _ in range(h)]
    mul(A11_inverse_A12, S22_inverse, A11_inverse_A12_S22_inverse, 0, 0, 0, 0, 0, 0, h)

    S22_inverse_A21_A11_inverse = [[0 for _ in range(h)] for _ in range(h)]
    mul(S22_inverse, A21_A11_inverse, S22_inverse_A21_A11_inverse, 0, 0, 0, 0, 0, 0, h)

    result = [[0 for _ in range(n)] for _ in range(n)]
    mul(A11_inverse_A12_S22_inverse, A21_A11_inverse, result, 0, 0, 0, 0, 0, 0, h)

    for i in range(n):
        for j in range(n):
            # result11
            if i < h and j < h:
                result[i][j] += A11_inverse[i][j]
                flop_counter = flop_counter + 1
            # result12
            if i < h <= j:
                result[i][j] = -A11_inverse_A12_S22_inverse[i][j-h]
            # result21
            if i >= h > j:
                result[i][j] = -S22_inverse_A21_A11_inverse[i-h][j]
            # result22
            if i >= h and j >= h:
                result[i][j] =  S22_inverse[i-h][j-h]

    return result


def print_matrix(A):
    for row in A:
        for el in row:
            print(f"{el:3.3f}", end=" ")
        print()

def save_plots(results, ylabel, filename):
    results = np.array(results)
    plt.figure(figsize=(60, 30))
    plt.subplot(1, 2, 1)
    plt.plot(results)
    plt.xlabel("K [2^K - rozmiar macierzy]")
    plt.ylabel(ylabel)
    plt.subplot(1, 2, 2)
    plt.plot(np.log(results))
    plt.xlabel("K [2^K - rozmiar macierzy]")
    plt.ylabel(f'Log {ylabel}')
    
    plt.savefig(filename)


if __name__ == '__main__':
    times = []
    flops = []

    for k in range(0, 9):
        print(k)
        flop_counter = 0
        n = 2**k
        A = [[random.randint(1, 4) for _ in range(n)] for _ in range(n)]
        start_time = time.time()
        A_inverse = inverse(A)
        times.append(time.time() - start_time)
        flops.append(flop_counter)
        C = [[0 for _ in range(n)] for _ in range(n)]
        mul(A, A_inverse, C, 0,0,0,0,0,0,n)
    
    print(times)
    print(flops)
    save_plots(times, 'Time [s]', 'time.jpg')
    save_plots(flops, 'Liczba operacji zmienno-przecinkowych', 'flops.jpg')