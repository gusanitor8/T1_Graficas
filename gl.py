import struct
from collections import namedtuple
import numpy as np

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b*255), 
                  int(g*255),
                  int(r*255)])

TRIANGLES = 3

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()

        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

        self.vertexShader = None
        self.fragmentShader = None

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)

    def glModelMatrix(sel, translate = (0,0,0), scale = (1,1,1)):
        translation= np.matrix([[1,0,0,translate[0]],
                                       [0,1,0,translate[1]],
                                       [0,0,1,translate[2]],
                                       [0,0,0,1]])
        
        scaleMat = np.matrix([[1,0,0,translate[0]],
                                        [0,1,0,translate[1]],
                                        [0,0,1,translate[2]],
                                        [0,0,0,1]])
        
        self.Model = translation * scaleMat
        pass

    def glRender(self):
        transformedVerts = []
        for vert in self.vertexBuffer:
            if self.vertexShader:
                transformedVerts.append(self.vertexShader(vertex=vert))
            else:
                transformedVerts.append(vert)

            primitives = self.glPrimitiveAssembly(transformedVerts)

            for prim in primitives:
                if self.primitiveType == TRIANGLES:
                    self.glTriangle(prim[0], prim[1], prim[2])
    
    def glPrimitiveAssembly(self,tVerts):
        primitives = []

        if self.primitiveType == TRIANGLES:
            triangle = [] 
            
            for i in range(0, len(tVerts), 3):
                triangle = []
                triangle.append(tVerts[i])
                triangle.append(tVerts[i+1])
                triangle.append(tVerts[i+2]) 
                primitives.append(triangle)

        return primitives

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]
        
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y]=clr or self.currColor

    def glLine(self, v0, v1, clr = None):
        #Bresenham line algorithm
        #y = mx + b
        
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)
        
        if (x0 == x1 and y0 == y1):
            self.glPoint(x0, int(y0))
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        steep = dy > dx
        
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0
        
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, clr or self.currColor)
            else:
                self.glPoint(x, y, clr or self.currColor)
                
            offset += m
            
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                    
                limit += 1

    def glTriangle(self, v0, v1, v2, clr = None):
        self.glLine(v0, v1, clr or self.currColor)
        self.glLine(v1, v2, clr or self.currColor)
        self.glLine(v2, v0, clr or self.currColor)

        
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height * 3)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])