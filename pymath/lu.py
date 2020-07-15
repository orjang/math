
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


def _forward_substitute(P, L, B):
    n = L.shape.rows
    h = B.shape.columns
    PB = P @ B
    Y = Matrix(n, h)
    for j in range(h):
        Y[0, j] = PB[0, j] / L[0, 0]
        for i in range(1, n):
            s = sum(L[i, k] * Y[k, j] for k in range(i - 1))
            Y[i, j] = (PB[i, j] - s) / L[i, i]

    return Y


def _backward_substitute(U, Y):
    n = U.shape.rows
    h = Y.shape.columns
    m = n - 1
    X = Matrix(n, h)
    for j in range(h):
        X[m, j] = Y[m, j] / U[m, m]
        for i in range(m, 0, -1):
            s = sum(U[i - 1, k] * X[k, j] for k in range(i, n))
            X[i - 1, j] = (Y[i - 1, j] - s) / U[i - 1, i - 1]

    return X


def solve(A, B):
    P, L, U = lu(A)
    Y = _forward_substitute(P, L, B)
    X = _backward_substitute(U, Y)

    return X


def main():
    M = Matrix([[0, 1, 0],
                [-8, 8, 1],
                [2, -2, 0]])

    B = Matrix([[1, 2], [2, 3], [4, 0.5]])

    X = solve(M, B)
    print(f'B: {B}\n')
    print(f'X: {X}\n')
    print(f'M @ X: {M @ X}\n')


if __name__ == '__main__':
    main()
