import pipes
import struct
from PIL import Image

class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, width, height):
        try:
            image = Image.open('output.bmp')  # Ruta del archivo BMP
        except FileNotFoundError:
            print("Archivo no encontrado")
            return


        # Creamos un buffer para almacenar el color de los píxeles de la nueva imagen
        framebuffer = []

        # Recorremos cada píxel de la imagen BMP cargada
        for y in range(height):
            row = []
            for x in range(width):
                # Tomamos el color del píxel de la imagen original
                r, g, b = pipes[x, y]

                # Aplicamos una transformación (invertir los colores)
                modified_color = (255 - r, 255 - g, 255 - b)

                row.append(modified_color)
            framebuffer.append(row)

        # Guardamos el framebuffer como una nueva imagen BMP
        self.writebmp("output_modified.bmp", width, height, framebuffer)

    def writebmp(self, filename, width, height, framebuffer):
        with open(filename, "wb") as f:
            # BMP Header
            f.write(b'B')
            f.write(b'M')
            f.write(struct.pack('=l', 54 + width * height * 3))  # File size
            f.write(b'\x00\x00')  # Unused
            f.write(b'\x00\x00')  # Unused
            f.write(b'\x36\x00\x00\x00')  # Offset to pixel array

            # DIB Header
            f.write(b'\x28\x00\x00\x00')  # DIB header size
            f.write(struct.pack('=l', width))
            f.write(struct.pack('=l', height))
            f.write(b'\x01\x00')  # Number of color planes
            f.write(b'\x18\x00')  # Bits per pixel (24)
            f.write(b'\x00\x00\x00\x00')  # No compression
            f.write(struct.pack('=l', width * height * 3))  # Image size
            f.write(b'\x13\x0B\x00\x00')  # Horizontal resolution (2835 pixels per meter)
            f.write(b'\x13\x0B\x00\x00')  # Vertical resolution (2835 pixels per meter)
            f.write(b'\x00\x00\x00\x00')  # Number of colors in palette
            f.write(b'\x00\x00\x00\x00')  # Important colors

            # Pixel data (bottom to top)
            for y in range(height):
                for x in range(width):
                    f.write(struct.pack('=B', framebuffer[height - 1 - y][x][2]))  # Blue
                    f.write(struct.pack('=B', framebuffer[height - 1 - y][x][1]))  # Green
                    f.write(struct.pack('=B', framebuffer[height - 1 - y][x][0]))  # Red


class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            self.pixels = []

            for y in range(self.height):
                pixelRow = []

                for x in range(self.width):
                    b = image.read(1)[0] / 255  # Leer bytes directamente
                    g = image.read(1)[0] / 255
                    r = image.read(1)[0] / 255
                    pixelRow.append([r, g, b])

                self.pixels.append(pixelRow)

    def getColor(self, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return self.pixels[int(v * self.height)][int(u * self.width)]
        else:
            return None
