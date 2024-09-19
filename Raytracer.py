from gl import Raytracer, V3, _color
from obj import Obj, Texture
from figures import Sphere, Material

# Clase para gestionar el modelo del muñeco de nieve
class Snowman:
    def __init__(self):
        self.sclera = Material(diffuse=_color(1, 1, 1))
        self.pupil = Material(diffuse=_color(0, 0, 0))
        self.body = Material(diffuse=_color(0.90, 0.90, 0.90))
        self.nose = Material(diffuse=_color(1, 0.6, 0))
        self.smile = Material(diffuse=_color(0, 0, 0))  # Cambiar a negro
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
        # Separación aumentada para las esferas de la boca
        positions = [(-0.04, 0.09), (-0.015, 0.08), (0.015, 0.08), (0.04, 0.09)]
        for pos in positions:
            rtx.scene.append(Sphere(V3(pos[0], pos[1], -1), 0.006, self.smile))

    def add_buttons(self, rtx):
        positions = [(0, 0.025), (0, -0.2), (0, -0.4)]
        for pos in positions:
            rtx.scene.append(Sphere(V3(pos[0], pos[1], -2), 0.035, self.button))

# Tamaño de la ventana
width = 512
height = 512

# Crear el raytracer y el muñeco de nieve
rtx = Raytracer(width, height)
snowman = Snowman()

# Agregar componentes del muñeco de nieve a la escena
snowman.add_eyes(rtx)
snowman.add_body(rtx)
snowman.add_nose(rtx)
snowman.add_smile(rtx)
snowman.add_buttons(rtx)

# Renderizar la escena
rtx.glRender()
rtx.glFinish('output.bmp')
