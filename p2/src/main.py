## we received the best results with such value
L = 2**4
global add_ctr
global mul_ctr


def mul(A, B, C, ax, ay, bx, by, cx, cy, n):
    global add_ctr
    global mul_ctr
    if (n <= L):
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    if (C[cx + a][cy + b]):
                        add_ctr = add_ctr + 1
                    C[cx + a][cy + b] += A[ax + a][ay + c] * B[bx + c][bx + b]
                    mul_ctr = mul_ctr + 1
    else:
        h = int(n/2)
        mul(A, B, C, ax, ay, bx, by, cx, cy, h)
        mul(A, B, C, ax, ay + h, bx + h, by, cx, cy, h)
        mul(A, B, C, ax, ay, bx, by + h, cx, cy + h, h)
        mul(A, B, C, ax, ax + h, bx+h, bx+h, cx, cy+h, h)
        mul(A, B, C, ax+h, ay, bx, by, cx+h, cy, h)
        mul(A, B, C, ax+h, ay+h, bx+h, by, cx+h, cy, h)
        mul(A, B, C, ax+h, ay, bx, by+h, cx+h, cy+h, h)
        mul(A, B, C, ax+h, ay+h, bx+h, by+h, cx+h, cy+h, h)


if __name__ == '__main__':
    k = 7
    n = 2**k
    add_ctr = 0
    mul_ctr = 0
    A = [[1 for _ in range(n)] for _ in range(n)]
    B = [[2 for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]

    mul(A, B, C, 0, 0, 0, 0, 0, 0, n)
    print(C)
    print(add_ctr)
    print(mul_ctr)
