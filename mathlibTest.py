from mathlib import MatrixProduct, MatrixVectorProduct
import numpy as np
from pprint import pprint

def test_MatrixProduct():
    A = [[1, -2, -1, 3], [-1, 3, -2, -2], [2, 0, 1, 1], [1, -2, 2, 3]]
    B = [[3, 1, 3, 0], [1, 2, 3, 4], [2, 1, 3, -1], [1, 1, 0, 1]]
    C = [[1, 0, 1, 1], [2, 1, 3, 0], [3, 2, 0, 3], [2, 0, 1, 0]]
    result = MatrixProduct(A, MatrixProduct(B, C))

    result = np.matrix(result)
    numpy = np.matrix(A) * np.matrix(B) * np.matrix(C)
    pprint (result)
    pprint(numpy)

    if result.all() == numpy.all():
        print("MatrixProduct passed")

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