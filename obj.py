import struct

def _color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Obj:
    def __init__(self, filename):
        # Usamos el contexto de "with" para manejar el archivo
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        self._parse_obj()

    def _parse_obj(self):
        # Procesa las líneas del archivo
        for line in self.lines:
            if not line.strip():
                continue  # Salta líneas vacías
            
            prefix, value = self._split_line(line)
            if prefix == "v":  # Vértices
                self.vertices.append(self._parse_floats(value))
            elif prefix == "vt":  # Coordenadas de textura
                self.texcoords.append(self._parse_floats(value, 2))
            elif prefix == "vn":  # Normales
                self.normals.append(self._parse_floats(value))
            elif prefix == "f":  # Caras
                self.faces.append(self._parse_faces(value))

    def _split_line(self, line):
        if ' ' in line:
            return line.split(' ', 1)
        return None, None  # Evitar error si no hay espacios


    def _parse_floats(self, value, count=None):
        """Convierte una cadena de valores flotantes en una lista.
        Si count está especificado, devuelve solo esa cantidad de elementos."""
        floats = list(map(float, value.split()))
        return floats[:count] if count else floats

    def _parse_faces(self, value):
        """Parsea las caras (f) del archivo OBJ."""
        return [list(map(int, vert.split('/'))) for vert in value.split()]

class Texture:
    def __init__(self, filename):
        self.filename = filename
        self.pixels = []
        self._read_texture()

    def _read_texture(self):
        with open(self.filename, "rb") as image:
            header_size = self._get_header_size(image)
            self.width, self.height = self._get_dimensions(image)
            self._read_pixels(image, header_size)

    def _get_header_size(self, image):
        image.seek(10)
        return struct.unpack('=l', image.read(4))[0]

    def _get_dimensions(self, image):
        image.seek(18)  # 14 + 4 es la posición para leer ancho y alto
        width = struct.unpack('=l', image.read(4))[0]
        height = struct.unpack('=l', image.read(4))[0]
        return width, height

    def _read_pixels(self, image, header_size):
        image.seek(header_size)
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self._read_color(image))
            self.pixels.append(row)

    def _read_color(self, image):
        b = image.read(1)[0] / 255
        g = image.read(1)[0] / 255
        r = image.read(1)[0] / 255
        return _color(r, g, b)


    def get_color(self, tx, ty):
        """Obtiene el color en las coordenadas de textura (tx, ty)."""
        if 0 <= tx < 1 and 0 <= ty < 1:
            x = int(tx * self.width)
            y = int(ty * self.height)
            return self.pixels[y][x]
        return _color(0, 0, 0)
