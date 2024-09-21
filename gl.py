# gl.py
import struct
from camera import Camera # type: ignore
from math import tan, pi
import numpy as np
from MatL import ml
  


WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)

# Utilidades para escribir archivos binarios
def char(c): return struct.pack("=c", c.encode("ascii"))
def word(w): return struct.pack("=h", w)
def dword(d): return struct.pack("=l", d)
def _color(r, g, b):
    return (int(r * 255), int(g * 255), int(b * 255))

class Snowman(object):
    def add_eyes(self, rtx):
        rtx.scene.append(np.where(V3(-0.05, 0.31, -2), 0.025, self.sclera))
        rtx.scene.append(np.where(V3(0.05, 0.31, -2), 0.025, self.sclera))


class Raytracer(object):
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.scene = []  # Asegúrate de inicializar la escena
        self.frameBuffer = [[BLACK for _ in range(height)] for _ in range(width)]  # Inicializa el frameBuffer

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char('B'))
            file.write(char('M'))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    file.write(bytes([color[2], color[1], color[0]]))  # Guarda los colores en formato BGR

    def render(self):
        # Lógica para renderizar la escena
        self.glGenerateFrameBuffer('output.bmp')  # Genera el archivo BMP



    def glRender(self):
        # Aquí implementas el renderizado de la escena
        pass

class V3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"V3({self.x}, {self.y}, {self.z})"



class RendererRT:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        self.camera = Camera()
        self.glViewport(0, 0, self.width, self.height)
        self.glProjection()
        
        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()
        self.scene = []
    

    # Definir el viewport
    def glViewport(self, x, y, width, height):
        self.vpX, self.vpY = int(x), int(y)
        self.vpWidth, self.vpHeight = width, height

    # Proyección perspectiva
    def glProjection(self, n=0.1, f=1000, fov=60):
        self.nearPlane, self.farPlane = n, f
        self.fov = fov * pi / 180
        aspectRatio = self.vpWidth / self.vpHeight
        
        self.topEdge = tan(self.fov / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

    # Colores
    def glColor(self, r, g, b):
        self.currColor = [min(1, max(0, v)) for v in (r, g, b)]

    def glClearColor(self, r, g, b):
        self.clearColor = [min(1, max(0, v)) for v in (r, g, b)]

    def glClear(self):
        # Llenar la pantalla con el color de fondo
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)
        self.frameBuffer = [[self.clearColor[:] for _ in range(self.height)]
                            for _ in range(self.width)]

    # Dibuja un punto en la pantalla
    def glPoint(self, x, y, color=None):
        x, y = round(x), round(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    # Generar archivo BMP
    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            file.write(char("B") + char("M"))
            file_size = 14 + 40 + (self.width * self.height * 3)
            file.write(dword(file_size) + dword(0) + dword(14 + 40))
            file.write(dword(40) + dword(self.width) + dword(self.height))
            file.write(word(1) + word(24) + dword(0))
            file.write(dword(self.width * self.height * 3) + dword(0) * 4)
            
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    file.write(bytes([color[2], color[1], color[0]]))

    # Método para lanzar rayos
    def glCastRay(self, orig, direction):
        for obj in self.scene:
            if obj.ray_intersect(orig, direction):
                return True
        return False

    # Renderizado de la escena
    def glRender(self):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                pX = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                pY = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                pX *= self.rightEdge
                pY *= self.topEdge

                direction = [pX, pY, -self.nearPlane]
                direction = ml.norm(V3(*direction))  # Usa tu función de normalización

                if self.glCastRay(self.camera.translate, direction):
                    self.glPoint(x, y)

        