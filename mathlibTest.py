from pprint import pprint

import numpy as np

from mathlib import InverseMatrix, MatrixProduct, MatrixVectorProduct


def test_MatrixProduct():
    A = [[1, -2, -1, 3], [-1, 3, -2, -2], [2, 0, 1, 1], [1, -2, 2, 3]]
    B = [[3, 1, 3, 0], [1, 2, 3, 4], [2, 1, 3, -1], [1, 1, 0, 1]]
    C = [[1, 0, 1, 1], [2, 1, 3, 0], [3, 2, 0, 3], [2, 0, 1, 0]]
    D = [
        [4, 7, 2, 3],
        [0, 5, 9, 1],
        [6, 8, 2, 4],
        [3, 1, 7, 5]

    ]
    result = MatrixProduct(A, MatrixProduct(B, MatrixProduct(C, D)))

    result = np.matrix(result)
    numpy = np.matrix(A) * np.matrix(B) * np.matrix(C) * np.matrix(D)
    pprint(result)
    pprint(numpy)

    if result.all() == numpy.all():
        print("MatrixProduct passed")

test_MatrixProduct()

def test_MatrixVectorProduct():
    A = [[1, -2, -1, 3], [-1, 3, -2, -2], [2, 0, 1, 1], [1, -2, 2, 3]]
    v = [3, 1, 3, 0]
    result = MatrixVectorProduct(A, v)

    result = np.matrix(result)
    numpy = np.matrix(A) @ v
    pprint(result)
    pprint(numpy)

    if result.all() == numpy.all():
        print("MatrixVectorProduct passed")

test_MatrixVectorProduct()

def test_InverseMatrix():
    A = [[1, -2, -1, 3], [-1, 3, -2, -2], [2, 0, 1, 1], [1, -2, 2, 3]]
    res = InverseMatrix(A)

    res = np.matrix(res)
    pprint(res)
    numpy = np.linalg.inv(A)
    pprint(numpy)
    if res.all() == numpy.all():
        print("Inverse passed")


test_InverseMatrix()
