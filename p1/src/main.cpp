#include <iostream>
#include <iterator>
#include <chrono>

const int l = 1 << 9;
const int k = 1 << 9;
int A[k][k];
int B[k][k];
int C[k][k];
long long add_ctr = 0;
long long mul_ctr = 0;

void mul(int ax, int ay, int bx, int by, int cx, int cy, int n){
    if (n <= l) {
        for (int a = 0; a < n; a++)
            for (int b = 0; b < n; b++)
                for (int c = 0; c < n; c++){
                    if (C[cx + a][cy + b])
                        add_ctr++;
                    C[cx + a][cy + b] += A[ax + a][ay + c] * B[bx + c][bx + b];
                    mul_ctr++;
                }
        return;
    }
    int h = n/2;
    mul(ax, ay, bx, by, cx, cy, h);
    mul(ax, ay + h, bx + h, by, cx, cy, h);
    mul(ax, ay, bx, by + h, cx, cy + h, h);
    mul(ax, ax + h, bx+h, bx+h, cx, cy+h, h);
    mul(ax+h, ay, bx, by, cx+h, cy, h);
    mul(ax+h, ay+h, bx+h, by, cx+h, cy, h);
    mul(ax+h, ay, bx, by+h, cx+h, cy+h, h);
    mul(ax+h, ay+h, bx+h, by+h, cx+h, cy+h, h);
}

int main() {
    for(int i = 0; i < k; i++)
        for(int j = 0; j < k; j++){
            A[i][j] = 1;
            B[i][j] = 2;
            C[i][j] = 0;
        }
    int n = k;
    auto start = std::chrono::high_resolution_clock::now();
    mul(0, 0, 0, 0, 0, 0, n);
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << elapsed.count() << std::endl;
    // std::cout << add_ctr + mul_ctr << std::endl;
    return 0;
}
