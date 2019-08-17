import sys
from numbers import Rational

from matrix import Matrix, argmax


def pivot_matrix(M):
    n = M.shape.rows
    im = Matrix.identity(n)
    for j in range(n):
        row = argmax(M.column(j), j)
        if row != j:
            im = im.exchange_rows(row, j)

    return im


def lu(M, tol=1e-15):
    n = M.shape.rows
    L = Matrix(n, n)
    U = Matrix(n, n)
    P = pivot_matrix(M)
    PA = P @ M
    for j in range(n):
        L[j, j] = 1
        for i in range(j + 1):
            s1 = sum(U[k, j] * L[i, k] for k in range(i))
            U[i, j] = PA[i, j] - s1

        for i in range(j, n):
            s2 = sum(U[k, j] * L[i, k] for k in range(j))
            if abs(U[j, j]) < tol:
                raise ValueError('matrix is singular')
            L[i, j] = (PA[i, j] - s2) / U[j, j]

    return P, L, U
