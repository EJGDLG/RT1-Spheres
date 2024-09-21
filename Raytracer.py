import pygame
from pygame.locals import *
from gl import Camera, Raytracer, V3, _color
from obj import Obj, Texture  # type: ignore
from fg import Sphere, Material  # Cambié 'fg' a 'figures'

# Clase Snowman para crear el muñeco de nieve

class light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class Material:
    def __init__(self, diffuse, spec=0):  # Asegúrate de definir 'spec' con un valor por defecto
        self.diffuse = diffuse
        self.spec = spec

class Camera:
    def __init__(self, pos, lookAt):
        self.position = pos
        self.lookAt = lookAt


class Snowman:
    def __init__(self):
        self.sclera = Material(diffuse=_color(255, 255, 255))  # Asegúrate de que 'spec' esté manejado
        self.pupil = Material(diffuse=_color(0, 0, 0))
        self.body = Material(diffuse=_color(230, 230, 230))
        self.nose = Material(diffuse=_color(255, 120, 0))
        self.smile = Material(diffuse=_color(0, 0, 0))
        self.button = Material(diffuse=_color(0, 0, 0))

    def add_eyes(self, rtx):
        rtx.scene.append(Sphere(V3(-0.05, 0.31, -2), 0.025, self.sclera))
        rtx.scene.append(Sphere(V3(0.05, 0.31, -2), 0.025, self.sclera))
        rtx.scene.append(Sphere(V3(-0.03, 0.16, -1), 0.008, self.pupil))
        rtx.scene.append(Sphere(V3(0.020, 0.16, -1), 0.008, self.pupil))

    def add_body(self, rtx):
        rtx.scene.append(Sphere(V3(0, 0.35, -3), 0.25, self.body))
        rtx.scene.append(Sphere(V3(0, -0.10, -3), 0.30, self.body))
        rtx.scene.append(Sphere(V3(0, -0.60, -3), 0.40, self.body))

    def add_nose(self, rtx):
        rtx.scene.append(Sphere(V3(0, 0.25, -2), 0.03, self.nose))

    def add_smile(self, rtx):
        positions = [(-0.04, 0.09), (-0.015, 0.08), (0.015, 0.08), (0.04, 0.09)]
        for pos in positions:
            rtx.scene.append(Sphere(V3(pos[0], pos[1], -1), 0.006, self.smile))

    def add_buttons(self, rtx):
        positions = [(0, 0.025), (0, -0.2), (0, -0.4)]
        for pos in positions:
            rtx.scene.append(Sphere(V3(pos[0], pos[1], -2), 0.035, self.button))

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana
width = 512
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

# Crear el raytracer y el muñeco de nieve
rtx = Raytracer(width, height, screen)
snowman = Snowman()

# Agregar partes del muñeco de nieve a la escena del raytracer
snowman.add_eyes(rtx)
snowman.add_body(rtx)
snowman.add_nose(rtx)
snowman.add_smile(rtx)
snowman.add_buttons(rtx)

# **Ajustar la iluminación**
light = light(position=V3(-5, 5, -10), intensity=1.2)

# **Posicionar la cámara**
camera = Camera(pos=V3(0, 0, -6), lookAt=V3(0, 0, 0))  # Asegúrate de que esto coincida con la definición de tu Camera


# Renderizar la escena
rtx.glRender()  # Cambié 'render' a 'glRender' para coincidir con tu implementación
rtx.glFinish('output.bmp')  # Asegúrate de guardar la imagen en formato BMP

# Convertir la imagen generada en un formato compatible con Pygame
bmp_surface = pygame.image.load('output.bmp')

# Bucle principal de Pygame
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    # Dibujar la escena raytraced en la pantalla de Pygame
    screen.blit(bmp_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
