from mathlib import MatrixProduct, MatrixVectorProduct


def vertexShader(vertex, **kwargs):
    # Para cada vertice

    modelMatrx = kwargs["modelMatrix"]
    viewMatrx = kwargs["viewMatrix"]
    projectionMatrx = kwargs["projectionMatrix"]
    viewportMatrx = kwargs["viewportMatrix"]

    vt = [vertex[0], vertex[1], vertex[2], 1]



    vt = MatrixVectorProduct(
        MatrixProduct(
            viewportMatrx,
            MatrixProduct(
                projectionMatrx,
                MatrixProduct(
                    viewMatrx,
                    modelMatrx
                )
            )
        ),
        vt
    )

    """
    vt = MatrixVectorProduct(
                MatrixProduct(
                    viewMatrx,
                    modelMatrx
                ),
        vt
    )
    """
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    print(vt)

    return vt
