import struct
from collections import namedtuple
from Obj import Obj
from mathlib import matrix_multiplication, barycentricCoords, inverseMatrix, PI
from math import sin, cos, tan
import numpy as np
from texture import Texture

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

class Model(object):
    def __init__(self,filename, translate = (0,0,0), scale = (1,1,1), rotate = (0,0,0)):
        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale       

    def loadTexture(self, textureName):
        self.texture = Texture(textureName)

class Renderer(object):
    # Constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

        self.activeTexture = None
        
        self.glViewPort(0,0,width,height)
        self.glCamMatrix()
        self.glProjectionMatrix()

        self.directionalLight = (1,0,0)

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)
       
    def glPrimitiveAssembly(self, transformedVertices, tTexCoords, normals):
        # Assembly the vertices into points, lines or triangles
        primitives = []

        if self.primitiveType == TRIANGLES:
            for i in range(0, len(transformedVertices), 3):                
                triangle = [
                    #verts
                    transformedVertices[i],
                    transformedVertices[i+1],
                    transformedVertices[i+2],

                    #texCoords
                    tTexCoords[i],
                    tTexCoords[i + 1],
                    tTexCoords[i + 2],

                    #normals
                    normals[int(i/3)]

                ]
                primitives.append(triangle)
    
        return primitives

    # Clear the screen
    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)
    
    # Clear the screen
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[float('inf') for y in range(self.height)] for x in range(self.width)]
        
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

    def glLoadModel(self, filename, textureName, translate = (0,0,0), scale = (1,1,1), rotate = (0,0,0)):
        
        model = Model(filename, translate, scale, rotate)
        model.loadTexture(textureName)
        self.objects.append(model)        
        
    # Draw a triangle
    def glTriangle(self, A, B, C, clr = None):
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B

        self.glLine(A, B, clr or self.currColor)
        self.glLine(B, C, clr or self.currColor)
        self.glLine(C, A, clr or self.currColor)

        def flatBottom(vA, vB, vC):
            try:
                mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
            except:
                pass
            else:
                x0=vB[0]
                x1=vC[0]

                for y in range(int(vB[1]), int(vA[1])):
                    self.glLine((x0,y), (x1,y), clr or self.currColor)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA, vB, vC):
            try:
                mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
                mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
            except:
                pass
            else:
                x0=vA[0]
                x1=vB[0]

                for y in range(int(vA[1]), int(vC[1]), -1):
                    self.glLine((x0,y), (x1,y), clr or self.currColor)
                    x0 -= mCA
                    x1 -= mCB

        if B[1] == C[1]:
            #parte plana abajo
            flatBottom(A, B, C)
            
        elif A[1] == B[1]:
            #parte plana arriba
            flatTop(A, B, C)
            
        else:
            #dibujar ambos casos
            #vertice D
            #teorema del intercepto
            D = (A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1])
            flatBottom(A, B, D)
            flatTop(B, D, C)
            
    def glTriangle_bc(self, A, B, C, vtA, vtB, vtC, triangleNormal, clr = None):
        minX = round(min(A[0],B[0],C[0]))
        maxX = round(max(A[0],B[0],C[0]))
        minY = round(min(A[1],B[1],C[1]))
        maxY = round(max(A[1],B[1],C[1]))

        colorA = (1,0,0)
        colorB = (0,1,0)
        colorC = (0,0,1)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = (x,y)
                u,v,w = barycentricCoords(A,B,C,P)
                if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1 and x < len(self.zbuffer) and y < len(self.zbuffer[0]):
                    z = u * A[2] + v * B[2] + w * C[2]


                    if len(self.zbuffer) > x and x >= 0 and len(self.zbuffer[0]) > y and y >= 0:
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                u * vtA[1] + v * vtB[1] + w * vtC[1])

                            if self.fragmentShader != None:
                                

                                colorP = self.fragmentShader(texcoords = uvs,
                                                            texture = self.activeTexture,
                                                            triangleNormal = triangleNormal,
                                                            dLight = self.directionalLight) 
                                

                                self.glPoint(x,y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                colorP = self.currColor
                                self.glPoint(x,y, colorP)

                            # colorP = color(u * colorA[0] + v * colorB[0] + w * colorC[0],
                            #                u * colorA[1] + v * colorB[1] + w * colorC[1],
                            #                u * colorA[2] + v * colorB[2] + w * colorC[2]) 

    def glViewPort(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

        self.vpMatrix = [[width/2,0,0, x + width/2],
                         [0,height/2,0,y + height/2],
                         [0,0,0.5,0.5],
                         [0,0,0,1]]
        


    def glCamMatrix(self, translate = (0,0,0), rotate = (0,0,0)):       
        self.camMatrix = self.glModelMatrix(translate = translate, rotate = rotate)
        
        self.viewMatrix = inverseMatrix(self.camMatrix)
    
    def glProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        aspectRatio = self.vpWidth / self.vpHeight
        t = tan((fov * PI / 180) / 2) * n
        r = t * aspectRatio

        self.projectionMatrix = [[n/r,0,0,0],
                                 [0,n/t,0,0],
                                 [0,0,-(f+n)/(f-n),-2*f*n/(f-n)],
                                 [0,0,-1,0]]


    def glModelMatrix(self, translate = (0,0,0), scale = (1,1,1), rotate = (0,0,0)):
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

        xRotationMatrix = [
            [1,0,0,0],
            [0,cos(rotate[0]),-sin(rotate[0]),0],
            [0,sin(rotate[0]),cos(rotate[0]),0],
            [0,0,0,1]
        ]

        yRotationMatrix = [
            [cos(rotate[1]),0,sin(rotate[1]),0],
            [0,1,0,0],
            [-sin(rotate[1]),0,cos(rotate[1]),0],
            [0,0,0,1]
        ]

        zRotationMatrix = [
            [cos(rotate[2]),-sin(rotate[2]),0,0],
            [sin(rotate[2]),cos(rotate[2]),0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

        rotationMatrix = matrix_multiplication(matrix_multiplication(xRotationMatrix, yRotationMatrix), zRotationMatrix)
        
        return matrix_multiplication(matrix_multiplication(translation, rotationMatrix), scaleMatrix)

    def glRender(self):
        transformedVerts = []
        texcoords = []
        normals = []

        for model in self.objects:

            self.activeTexture = model.texture
            modelMatrix = self.glModelMatrix(model.translate, model.scale, model.rotate)

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                triangleNormal = np.cross(np.subtract(v1,v0), np.subtract(v2,v0))
                triangleNormal = triangleNormal / np.linalg.norm(triangleNormal)
                normals.append(triangleNormal)
                if vertCount == 4:
                    triangleNormal1 = np.cross(np.subtract(v2,v0), np.subtract(v3,v0))
                    triangleNormal1 = triangleNormal1 / np.linalg.norm(triangleNormal1)
                    normals.append(triangleNormal1)
                
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                if self.vertexShader:
                    v0 = self.vertexShader(vertex = v0,
                                            modelMatrix = modelMatrix,
                                            viewMatrix = self.viewMatrix,
                                            projectionMatrix = self.projectionMatrix,
                                            vpMatrix = self.vpMatrix)
                    
                    v1 = self.vertexShader(vertex = v1,
                                            modelMatrix = modelMatrix,
                                            viewMatrix = self.viewMatrix,
                                            projectionMatrix = self.projectionMatrix,
                                            vpMatrix = self.vpMatrix)
                    
                    v2 = self.vertexShader(vertex = v2,
                                            modelMatrix = modelMatrix,
                                            viewMatrix = self.viewMatrix,
                                            projectionMatrix = self.projectionMatrix,
                                            vpMatrix = self.vpMatrix)
                    if vertCount == 4:
                        v3 = self.vertexShader(vertex = v3,
                                            modelMatrix = modelMatrix,
                                            viewMatrix = self.viewMatrix,
                                            projectionMatrix = self.projectionMatrix,
                                            vpMatrix = self.vpMatrix)

                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)

                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]

                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]
                
                texcoords.append(vt0)
                texcoords.append(vt1)
                texcoords.append(vt2)

                if vertCount == 4:
                    texcoords.append(vt0)
                    texcoords.append(vt2)
                    texcoords.append(vt3)

        # for vert in self.vertexBuffer:
        #     if self.vertexShader:
        #         transformedVerts.append(self.vertexShader(vertex = vert, modelMatrix = self.modelMatrix))
        #     else:
        #         transformedVerts.append(vert)

        primitives = self.glPrimitiveAssembly(transformedVerts, texcoords, normals)
        primitiveColor = self.currColor
        

        for primitive in primitives:
            if self.primitiveType == TRIANGLES:
                primitiveColor = self.currColor


                A = primitive[0]
                B = primitive[1]
                C = primitive[2]
                vtA = primitive[3]
                vtB = primitive[4]
                vtC = primitive [5]
                normal = primitive[6]

                self.glTriangle_bc(A, B, C, vtA, vtB, vtC, normal, primitiveColor)

    def glPointToV2(self, point):
        return V2(point[0], point[1])    

    def glFillPolygon(self, color = color(1,1,1)):
        fill = last = current = False

        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[0])):
                current = (self.pixels[x][y] == self.currColor) ##Este puede ser curr color o el color del borde
                if current and (not last):
                    fill = not fill

                if fill:
                    self.pixels[x][y] = color

                last = current

            fill = last = current = False

    def glFillPolygon(self,vertices, clr=None):
        if clr == None:
            clr = color(1, 1, 1)
        

        # Function to check if a point is inside the polygon using the ray casting algorithm
        def is_inside_polygon(x, y):
            odd_nodes = False
            j = len(vertices) - 1
            for i in range(len(vertices)):
                xi, yi = vertices[i]
                xj, yj = vertices[j]
                if yi < y and yj >= y or yj < y and yi >= y:
                    if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                        odd_nodes = not odd_nodes
                j = i
            return odd_nodes

        for x in range(len(self.pixels)):
            for y in range(len(self.pixels[0])):
                if is_inside_polygon(x, y):
                    self.pixels[x][y] = clr

    def gldrawPolygon(self, points, clr=None):
        for i in range(len(points)):
            v0 = self.glPointToV2(points[i])
            v1 = self.glPointToV2(points[(i + 1) % len(points)])
            self.glLine(v0, v1)
        self.glFillPolygon(vertices=points, clr=clr)

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