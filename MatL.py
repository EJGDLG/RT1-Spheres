import numpy as np
from math import pi, sin, cos, isclose
from collections import namedtuple


V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

# Producto punto entre dos vectores
def dotProduct(a, b):
    return sum(x * y for x, y in zip(a, b))

# Suma de dos vectores
def sumVectors(a, b):
    return [x + y for x, y in zip(a, b)]

# Resta de dos vectores
def subVectors(a, b):
    return [x - y for x, y in zip(a, b)]

# Producto cruz entre dos vectores
def crossProduct(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]

# Crear una matriz a partir de una lista de listas
def createMatrix(row, col, listOfLists, multi=1):
    return [[listOfLists[row * i + j] * multi for j in range(col)] for i in range(row)]

# Convertir grados a radianes
def deg2rads(degNum):
    return (degNum * pi) / 180

# Multiplicación de un vector por una matriz
def multiVecMatrix(Vector, Matrix):
    return [sum(Matrix[y][x] * Vector[x] for x in range(len(Vector))) for y in range(len(Matrix))]

# Multiplicación de dos matrices
def multyMatrix(Matrix1, Matrix2):
    return [[sum(Matrix1[i][k] * Matrix2[k][j] for k in range(len(Matrix2))) for j in range(len(Matrix2[0]))] for i in range(len(Matrix1))]

# Transposición de una matriz
def transpose(matrix):
    return list(map(list, zip(*matrix)))

# Determinante de una matriz 2x2
def getMatrixDeterminant2x2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]

# Determinante de una matriz NxN usando recursión
def getMatrixDeterminant(m):
    if len(m) == 2:
        return getMatrixDeterminant2x2(m)
    return sum((-1)**c * m[0][c] * getMatrixDeterminant([row[:c] + row[c+1:] for row in m[1:]]) for c in range(len(m)))

# Inversa de una matriz NxN
def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)
    if len(m) == 2:
        return [[m[1][1] / determinant, -m[0][1] / determinant],
                [-m[1][0] / determinant, m[0][0] / determinant]]

    cofactors = [[((-1)**(r+c)) * getMatrixDeterminant([row[:c] + row[c+1:] for row in (m[:r]+m[r+1:])]) for c in range(len(m))] for r in range(len(m))]
    cofactors = transpose(cofactors)
    return [[cofactors[r][c] / determinant for c in range(len(cofactors))] for r in range(len(cofactors))]

# Longitud de un vector 3D
def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2) ** 0.5

# Normalización de un vector 3D
def norm(v0):
    v0length = length(v0)
    if v0length == 0:
        return V3(0, 0, 0)
    return V3(v0.x / v0length, v0.y / v0length, v0.z / v0length)

# Función para calcular la primera columna de una lista
def firstItemFunction(a):
    return a[0][2]

# Función para calcular la segunda columna de una lista
def secondItemFunction(a):
    return a[1][2]

# Función para calcular la tercera columna de una lista
def thirdItemFunction(a):
    return a[2][2]

# Función para calcular la cuarta columna de una lista
def fourthItemFunction(a):
    return a[3][2]
def TranslationMatrix(tx, ty, tz):
    return [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]

def RotationMatrix(rx, ry, rz):
    rx = deg2rads(rx)
    ry = deg2rads(ry)
    rz = deg2rads(rz)
    
    # Rotación en X
    Rx = [
        [1, 0, 0, 0],
        [0, cos(rx), -sin(rx), 0],
        [0, sin(rx), cos(rx), 0],
        [0, 0, 0, 1]
    ]
    # Rotación en Y
    Ry = [
        [cos(ry), 0, sin(ry), 0],
        [0, 1, 0, 0],
        [-sin(ry), 0, cos(ry), 0],
        [0, 0, 0, 1]
    ]
    # Rotación en Z
    Rz = [
        [cos(rz), -sin(rz), 0, 0],
        [sin(rz), cos(rz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    return multyMatrix(multyMatrix(Rz, Ry), Rx)
# ml es simplemente una referencia a las funciones de este archivo
ml = {
    'dotProduct': dotProduct,
    'sumVectors': sumVectors,
    'subVectors': subVectors,
    'crossProduct': crossProduct,
    'createMatrix': createMatrix,
    'multiVecMatrix': multiVecMatrix,
    'multyMatrix': multyMatrix,
    'transpose': transpose,
    'getMatrixDeterminant': getMatrixDeterminant,
    'getMatrixInverse': getMatrixInverse,
    'length': length,
    'norm': norm
}

