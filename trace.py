#!/usr/bin/env python
# vim: set fileencoding=utf-8

import math
import numpy as np
import pylab as pl
from matplotlib import cm

class V3:

    __slots__ = ['x', 'y', 'z']

    def __init__(self, x_or_pair=(0,0,0), y=None, z=None):
        if y is not None:
            x_or_pair = x_or_pair, y, z
        self.x, self.y, self.z = x_or_pair

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        else:
            raise IndexError('3D vector index out of range')

    def __setitem__(self, idx, val):
        if idx == 0:
            self.x = val
        elif idx == 1:
            self.y = val
        elif idx == 2:
            self.z = val
        else:
            raise IndexError('3D vector index out of range')

    def __pos__(self, other):
        return V3(
            +self.x,
            +self.y,
            +self.z)

    def __neg__(self, other):
        return V3(
            -self.x,
            -self.y,
            -self.z)

    def __add__(self, other):
        return V3(
            self.x + other[0],
            self.y + other[1],
            self.z + other[2])

    def __radd__(self, other):
        return V3(
            other[0] + self.x,
            other[1] + self.y,
            other[2] + self.z)

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]

    def __sub__(self, other):
        return V3(
            self.x - other[0],
            self.y - other[1],
            self.z - other[2])

    def __rsub__(self, other):
        return V3(
            other[0] - self.x,
            other[1] - self.y,
            other[2] - self.z)

    def __iadd__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]

    def __mul__(self, other):
        return V3(
            self.x * other,
            self.y * other,
            self.z * other)

    def __rmul__(self, other):
        return V3(
            other * self.x,
            other * self.y,
            other * self.z)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other

    def __div__(self, other):
        return V3(
            self.x / other,
            self.y / other,
            self.z / other)

    def __rdiv__(self, other):
        return V3(
            other / self.x,
            other / self.y,
            other / self.z)

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other

    def mult(self, other):
        return V3(
            self.x * other[0],
            self.y * other[1],
            self.z * other[2])

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    @property
    def length(self):
        return np.sqrt(self.dot(self))

    @length.setter
    def set_length(self, length):
        self *= length / self.length

    @property
    def normalized(self):
        return self * (1 / np.sqrt(self.dot(self)))

class Ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class Sphere:

    def __init__(self, center, radius, color, emission):
        self.center = center
        self.radius = radius
        self.color = color
        self.emission = emission

    def get_intersector(self, origin):
        distant = self.center - origin
        radius2 = self.radius ** 2

        return lambda direction: calc_intersect(distant, radius2, direction)

    def intersect(self, ray):
        distant = self.center - ray.origin
        radius2 = self.radius ** 2
        return calc_intersect(distant, radius2, ray.direction)

    def get_hittor(self, origin):
        intersector = self.get_intersector(origin)

        def hittor(direction):
            depth = intersector(direction)
            if depth == 0:
                return None, None, None
            position = origin + direction * depth
            normal = (position - self.center).normalized
            return self, depth, position, normal

        return hittor

def calc_intersect(distant, radius2, direction):
    b = distant.dot(direction)
    det = b * b - distant.dot(distant) + radius2
    if det < 0:
        return 0
    det = math.sqrt(det)
    return b - det if b - det > 0 else b + det if b + det > 0 else 0
    
class Scene:

    def __init__(self, objs):
        self.objs = objs

    def get_hittor(self, origin):
        self.hittors = [obj.get_hittor(origin) for obj in self.objs]
        def hittor(direction):
            hitResult = (None, None, None, None)
            for hittor in self.hittors:
                result = hittor(direction)
                if result[0] is not None:
                    if hitResult[0] is None or result[0] < hitResult[0]:
                        hitResult = result
            return hitResult
        return hittor

camera = V3(0, 0, -2)
scene = Scene([
    Sphere(V3(-0.5, 0, 0), 1, 1, 0),
    Sphere(V3(0.5, 0, -0.5), 0.5, 0, 1),
    ])
hittor = scene.get_hittor(camera)

def radiance(direction, hittor=hittor, rescus=1):
    obj, depth, position, normal = hittor(direction)
    if depth is None:
        return 0

    if rescus <= 0:
        return obj.emission

    ndd = normal.dot(direction)
    return obj.emission - obj.color * ndd

    direction = direction - normal * (2 * normal.dot(direction))
    hittor = scene.get_hittor(position)
    return obj.emission + obj.color * radiance(direction, hittor, rescus-1)

def get_r_point(x, y):
    direction = V3(x, y, 1).normalized
    r = radiance(direction)
    return r

def render_image(cx, cy, d):
    x0, x1, y0, y1 = cx - d, cx + d, cy - d, cy + d
    y, x = np.ogrid[y0:y1:100j, x0:x1:100j]
    r = np.frompyfunc(get_r_point, 2, 1)(x, y).astype(np.float)
    return r

import time
t0 = time.time()
im = render_image(0, 0, 1)
t1 = time.time()
print 'Time Passed:', t1 - t0

pl.axis('off')
pl.imshow(im, cmap='gray')
pl.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
pl.show()
