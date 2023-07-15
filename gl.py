import struct
from collections import namedtuple
from matrixes import *
V2 = namedtuple('point', ['x','y'])
V3 = namedtuple('point', ['x','y','z'])
POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

# Write the BMP file 
def char(c):
    return struct.pack('=c', c.encode('ascii'))

# Write the BMP file
def word(w):
    return struct.pack('=h', w)

# Write the BMP file
def dword(d):
    return struct.pack('=l', d)

# Transform the color format from float to bytes
def color(r, g, b):
    return bytes([int(b*255), int(g*255), int(r*255)])

class Renderer(object):
    # Constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.glColor(1,1,1)

        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)
       
    def glPrimitiveAssembly(self, transformedVertices):
        # Assembly the vertices into points, lines or triangles
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(transformedVertices), 3):
                triangle = [
                    transformedVertices[i],
                    transformedVertices[i+1],
                    transformedVertices[i+2]
                ]
                primitives.append(triangle)
    
        return primitives

    # Clear the screen
    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)
    
    # Clear the screen
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]
        
    # Set the color
    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)
        
    # Draw a point
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels [x][y] = clr or self.currColor
            
    # Draw a line
    def glLine(self, v0, v1, clr = None):
        # Bressenham line algorith
        # y = mx+b
        
        #m = (v1.y-v0.y)/(v1.x-v0.x)
        #y = v0.y
        
        #for x in range(v0.x, v1.x+1):
        #   self.glPoint(x,int(y))
        #   y += m
            
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])
        

        # Si las coordenadas son las mismas, se dibuja un solo pixel
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        # Se verifica si la pendiente es mayor que 1 (Porque, si es así, saltaría pixeles)
        steep = dy > dx
        
        # Si la pendiente es mayor que 1 o menor que -1
        # entonces intercambiamos los valores de x y y
        # para reorientar la linea (Se dibuja vertical en vez de horizontal)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # Si el punto inicial es mayor que el punto final, se intercambian
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        # Se recalculan las diferencias
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0
        limit = 0.5
        
        m = dy/dx
        y = y0
        
        for x in range(x0, x1+1):
            # Si la pendiente es mayor que 1, se dibuja vertical
            if steep:
               self.glPoint(y, x, clr or self.currColor)
            else:
                self.glPoint(x, y, clr or self.currColor)
            
            offset += m
            
            if offset > limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1
        
    # Draw a triangle
    def glTriangle(self, A, B, C, clr = None):
        self.glLine(A, B, clr or self.currColor)
        self.glLine(B, C, clr or self.currColor)
        self.glLine(C, A, clr or self.currColor)

    def glModelMatrix(self, translate = (0,0,0), scale = (1,1,1)):
        translation = [
            [1,0,0,translate[0]],
            [0,1,0,translate[1]],
            [0,0,1,translate[2]],
            [0,0,0,1]
        ]

        scaleMatrix = [
            [scale[0],0,0,0],
            [0,scale[1],0,0],
            [0,0,scale[2],0],
            [0,0,0,1]
        ]

        self.modelMatrix = multiplyMatrices(translation, scaleMatrix)


    def glRender(self):
        transformedVerts = []
        for vert in self.vertexBuffer:
            if self.vertexShader:
                transformedVerts.append(self.vertexShader(vertex = vert, modelMatrix = self.modelMatrix))
            else:
                transformedVerts.append(vert)

        primitives = self.glPrimitiveAssembly(transformedVerts)
        primitiveColor = self.currColor
        if self.fragmentShader:
            primitiveColor = self.fragmentShader()
            primitiveColor = color(
                primitiveColor[0],
                primitiveColor[1],
                primitiveColor[2]
            )
     

        for primitive in primitives:
            if self.primitiveType == TRIANGLES:
                A = primitive[0]
                B = primitive[1]
                C = primitive[2]
                self.glTriangle(A, B, C, primitiveColor)

    # Export the BMP file
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B")) #BMP
            file.write(char("M")) #BMP
            file.write(dword(14 + 40 + (self.width * self.height * 3))) #size
            file.write(dword(0)) #reserved
            file.write(dword(14 + 40)) #pixel offset

            #InfoHeader
            file.write(dword(40)) #InfoHeader size
            file.write(dword(self.width)) #width
            file.write(dword(self.height)) #height
            file.write(word(1)) #planes
            file.write(word(24)) #bits per pixel
            file.write(dword(0)) #compression
            file.write(dword(self.width * self.height * 3)) #image size
            file.write(dword(0)) #x resolution
            file.write(dword(0)) #y resolution
            file.write(dword(0)) #n colors
            file.write(dword(0)) #important colors

            #ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])