import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    amb = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)
    return limit_color([x+y+z for x,y,z in zip(amb,diff,spec)])

def calculate_ambient(alight, areflect):
    return limit_color([int(x*y) for x,y in zip(alight,areflect)])

def calculate_diffuse(light, dreflect, normal):
    color = [int(x*y) for x,y in zip(light[1],dreflect)]
    pos = light[0]
    l = normalize(pos)
    n = normalize(normal)
    dot = dot_product(n, l)
    lim = limit_color([int(x*dot) for x in color])
    return lim


def calculate_specular(light, sreflect, view, normal):
    color = [x*y for x,y in zip(light[1],sreflect)]
    l = normalize(light[0])
    v = normalize(view)
    n = normalize(normal)
    a = [x*2*dot_product(n, l) for x in n]
    b = [x-y for x,y in zip(a,l)]
    c = [int(x*(dot_product(b,v)**8)) for x in color]
    if dot_product(n, l) <= 0:
        return [0,0,0]
    return limit_color(c)

def limit_color(color):
    for c in range(len(color)):
        if color[c] >= 255:
            color[c] = 255
        if color[c] <= 0:
            color[c] = 0

    return color

#vector functions
def normalize(vector):
    denom = (vector[0]**2 + vector[1]**2 + vector[2]**2) **0.5
    return [each/denom for each in vector]

def dot_product(a, b):
    return sum(x*y for x,y in zip(a,b))

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
