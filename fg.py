import numpy as np
from gl import WHITE # type: ignore
import MatL as ml # type: ignore

class Material:
    def __init__(self, diffuse=WHITE):
        self.diffuse = diffuse

class Intersect:
    def __init__(self, distance):
        self.distance = distance

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = ml.subVectors(self.center, orig)
        tca = ml.dotProduct(L, dir)
        d = (ml.length(L)**2 - tca**2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius**2 - d**2) ** 0.5
        t0 = tca - thc if tca - thc > 0 else tca + thc

        return Intersect(distance=t0) if t0 > 0 else None


    def ray_intersect(self, orig, dir):
        L = ml.subVectors(self.center, orig)
        tca = ml.dotProduct(L, dir)
        d2 = ml.length(L)**2 - tca**2

        if d2 > self.radius**2:
            return None

        thc = (self.radius**2 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        return Intersect(distance=t0)



        