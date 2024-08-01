from mathlib import MatrixVectorProduct


def vertexShader(vertex, **kwargs):
    # Para cada vertice

    modelMatrx = kwargs["modelMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]

    vt = MatrixVectorProduct(modelMatrx, vt)

    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt
