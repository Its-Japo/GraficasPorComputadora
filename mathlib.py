from math import cos, pi, sin


def MatrixProduct(A, B):
    result = [[x * 0 for x in range(len(A[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result


def MatrixVectorProduct(A, v):
    result = [0] * len(A)

    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i] += A[i][j] * v[j]

    return result


def Eliminate(r1, r2, col, target=0):
    fac = (r2[col] - target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]


def Gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i + 1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                raise ValueError("cant inverse matrix")

        for j in range(i + 1, len(a)):
            Eliminate(a[i], a[j], i)

    for i in range(len(a) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            Eliminate(a[i], a[j], i)

    for i in range(len(a)):
        Eliminate(a[i], a[i], i, target=1)

    return a


def InverseMatrix(A: list):
    tmp = [[] for _ in A]

    for i, j in enumerate(A):
        assert len(j) == len(A)
        tmp[i].extend(j + [0] * i + [1] + [0] * (len(A) - i - 1))

    Gauss(tmp)

    result = []
    for i in range(len(tmp)):
        result.append(tmp[i][len(tmp[i]) // 2:])

    return result


def TranslationMatrix(x, y, z):
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def ScaleMatrix(x, y, z):
    return [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]


def RotateMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180

    pitchMat = [
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1],
    ]

    yawMat = [
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1],
    ]

    rollMat = [
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return MatrixProduct(MatrixProduct(pitchMat, yawMat), rollMat)
