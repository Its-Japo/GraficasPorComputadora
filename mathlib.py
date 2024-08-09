from math import cos, pi, sin

class Matrix:
    def __init__(self, data):
        self.data = data

    def productoMatrices(self, objeto):
        mat1 = self.data
        mat2 = objeto.data
        result = [
            [0 for _ in range(len(mat2[0]))] for _ in range(len(mat1))
        ]
        for i in range(len(mat1)):
            for j in range(len(mat2[0])):
                for k in range(len(mat2)):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return Matrix(result)

    def productoPorVector(self, objeto):
        mat = self.data
        vec = objeto
        result = [0 for _ in range(len(mat))]

        for i in range(len(mat)):
            for j in range(len(vec)):
                result[i] += mat[i][j] * vec[j]

        return result

    def __mul__(self, objeto):
        if isinstance(objeto, Matrix):
            return self.productoMatrices(objeto)
        if isinstance(objeto, list):
            return self.productoPorVector(objeto)

    def transponer(self):
        mat = self.data
        return [list(row) for row in zip(*mat)]
    def getMinor(self, i, j):
        mat = self.data
        return [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]

    def determinante(self):
        mat = self.data
        if len(mat) == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

        det = 0

        for i in range(len(mat)):
            det += ((-1) ** i) * mat[0][i] * Matrix(self.getMinor(0, i)).determinante()
        return det

    def inversa(self):
        mat = self.data
        det = self.determinante()

        n = len(mat)

        if n == 2:
            return Matrix([[mat[1][1] / det, -1 * mat[0][1] / det],
                           [-1 * mat[1][0] / det, mat[0][0] / det]])

        cofactors = []
        for r in range(n):
            cofactorRow = []
            for c in range(n):
                minor = Matrix(self.getMinor(r, c))
                cofactorRow.append(((-1) ** (r + c)) * minor.determinante())
            cofactors.append(cofactorRow)

        cofactorMatrix = Matrix(cofactors)
        cofactors_transposed = cofactorMatrix.transponer()

        inverse_matrix = []
        for r in range(n):
            row = [value / det for value in cofactors_transposed[r]]
            inverse_matrix.append(row)

        return Matrix(inverse_matrix)


def TranslationMatrix(x, y, z):
    return Matrix([[1, 0, 0, x],
                   [0, 1, 0, y],
                   [0, 0, 1, z],
                   [0, 0, 0, 1],
                   ])


def ScaleMatrix(x, y, z):
    return Matrix([[x, 0, 0, 0],
                   [0, y, 0, 0],
                   [0, 0, z, 0],
                   [0, 0, 0, 1],
                   ])


def RotationMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180

    pitchMat = Matrix([
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1],
    ])

    yawMat = Matrix([
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1],
    ])

    rollMat = Matrix([
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll), cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    return pitchMat * yawMat * rollMat

def barycentricCoords(A, B, C, P):

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	if areaABC == 0:
		return None

	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC

	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None