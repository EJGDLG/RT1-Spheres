from MatL import TranslationMatrix, RotationMatrix, multyMatrix as MatrixMultiply, getMatrixInverse as InvertMatrix # type: ignore


class Camera(object):
    def __init__(self):
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def GetViewMatrix(self):
        # Creación de la matriz de traslación y rotación
        translateMat = TranslationMatrix(self.translate[0],
                                         self.translate[1],
                                         self.translate[2])

        rotateMat = RotationMatrix(self.rotate[0],
                                   self.rotate[1],
                                   self.rotate[2])

        camMatrix = MatrixMultiply(translateMat, rotateMat)

        # Aquí reemplaza np.linalg.inv con tu función personalizada de inversión
        invCamMatrix = InvertMatrix(camMatrix)
        
        return invCamMatrix
