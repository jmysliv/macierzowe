import random
import time
from copy import copy

import matplotlib.pyplot as plt
import numpy as np

"we received the best results with such value"
L = 2 ** 4
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
        h = int(n / 2)
        mul(A, B, C, ax, ay, bx, by, cx, cy, h)
        mul(A, B, C, ax, ay + h, bx + h, by, cx, cy, h)
        mul(A, B, C, ax, ay, bx, by + h, cx, cy + h, h)
        mul(A, B, C, ax, ay + h, bx + h, by + h, cx, cy + h, h)
        mul(A, B, C, ax + h, ay, bx, by, cx + h, cy, h)
        mul(A, B, C, ax + h, ay + h, bx + h, by, cx + h, cy, h)
        mul(A, B, C, ax + h, ay, bx, by + h, cx + h, cy + h, h)
        mul(A, B, C, ax + h, ay + h, bx + h, by + h, cx + h, cy + h, h)


def inverse(A):
    global flop_counter
    n = len(A)
    if n == 1:
        if A[0][0] == 0:
            return [[0]]
        return [[1 / A[0][0]]]
    h = int(n / 2)
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
    flop_counter = flop_counter + (h ** 2)

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
                result[i][j] = -A11_inverse_A12_S22_inverse[i][j - h]
            # result21
            if i >= h > j:
                result[i][j] = -S22_inverse_A21_A11_inverse[i - h][j]
            # result22
            if i >= h and j >= h:
                result[i][j] = S22_inverse[i - h][j - h]

    return result


def lu_factorization(A):
    global flop_counter
    n = len(A)
    if n == 2:
        a11 = A[0][0]
        a12 = A[0][1]
        a21 = A[1][0]
        a22 = A[1][1]

        l21 = a21 / a11
        flop_counter += 1
        L = [
            [1, 0],
            [l21, 1],
        ]

        U = [
            [a11, a12],
            [0, a22 - (l21 * a12)],
        ]
        return L, U

    h = n // 2

    a11 = copy([row[:h] for row in A[:h]])
    a12 = copy([row[h:] for row in A[:h]])
    a21 = copy([row[:h] for row in A[h:]])
    a22 = copy([row[h:] for row in A[h:]])
    l11, u11 = lu_factorization(a11)
    l11_inv = inverse(l11)
    u11_inv = inverse(u11)

    l21 = [[0 for _ in range(h)] for _ in range(h)]
    mul(a21, u11_inv, l21, 0, 0, 0, 0, 0, 0, h)
    a11_inv = inverse(a11)
    u12 = [[0 for _ in range(h)] for _ in range(h)]
    mul(l11_inv, a12, u12, 0, 0, 0, 0, 0, 0, h)

    tmp1 = [[0 for _ in range(h)] for _ in range(h)]
    mul(a11_inv, a12, tmp1, 0, 0, 0, 0, 0, 0, h)
    tmp2 = [[0 for _ in range(h)] for _ in range(h)]
    mul(a21, tmp1, tmp2, 0, 0, 0, 0, 0, 0, h)

    S = [[0 for _ in range(h)] for _ in range(h)]
    for i in range(0, h):
        for j in range(0, h):
            S[i][j] = a22[i][j] - tmp2[i][j]
            flop_counter += 1
    l22, u22 = lu_factorization(S)

    l = merge_matrices(
        [[0 for _ in range(n)] for _ in range(n)],
        l11,
        [[0 for _ in range(n)] for _ in range(n)],
        l21,
        l22,
    )
    u = merge_matrices(
        [[0 for _ in range(n)] for _ in range(n)],
        u11,
        u12,
        [[0 for _ in range(n)] for _ in range(n)],
        u22,
    )
    return l, u


def merge_matrices(A, a11, a12, a21, a22):
    n = len(A)
    half = n // 2
    for i in range(n):
        for j in range(n):
            if i < half:
                if j < half:
                    A[i][j] = a11[i][j]
                else:
                    A[i][j] = a12[i][j - half]
            else:
                if j < half:
                    A[i][j] = a21[i - half][j]
                else:
                    A[i][j] = a22[i - half][j - half]
    return A


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
    plt.ylabel(f"Log {ylabel}")

    plt.savefig(filename)


if __name__ == "__main__":
    times = []
    flops = []

    for k in range(1, 9):
        print(k)
        flop_counter = 0
        n = 2 ** k
        A = [[random.randint(1, 4) for _ in range(n)] for _ in range(n)]
        while np.linalg.matrix_rank(np.array(A)) < n:
            A = [[random.randint(1, 4) for _ in range(n)] for _ in range(n)]
        start_time = time.time()
        lu_factorization(A)
        times.append(time.time() - start_time)
        flops.append(flop_counter)

    print(times)
    print(flops)
    save_plots(times, "Time [s]", "time.jpg")
    save_plots(flops, "Liczba operacji zmienno-przecinkowych", "flops.jpg")
