from gl import Renderer, V2, V3, color
import shaders
import random

width = 512
height = 512

render = Renderer(width, height)
render.vertexShader = shaders.vertexShader
render.fragmentShader = shaders.fragmentShader

def output1():
    for x in range(0, width, 10):
        render.glLine(V2(0,0), V2(x,height-1))
    
    render.glFinish('output1.bmp')

def output2():
    for x in range(0, width, 10):
        render.glLine(V2(0,0), V2(x,height-1))

    for x in range(0, width, 10):
        render.glLine(V2(0, height - 1), V2(x, 0))

    render.glFinish('output2.bmp')

def output3():
    for x in range(0, width, 10):
        render.glLine(V2(0,0), V2(x,height-1))

    for x in range(0, width, 10):
        render.glLine(V2(0, height - 1), V2(x, 0))

    for y in range(0, height, 10):
        render.glLine(V2(0,0), V2(width-1,y))

    for y in range(0, height, 10):
        render.glLine(V2(0, width - 1), V2(height-1, y))

    render.glFinish('output3.bmp')

# Noise
def output4():
    for x in range(width):
        for y in range(height):
            if random.random() > 0.5:
                render.glPoint(x, y, color(random.random(), random.random(), random.random()))

    render.glFinish('output4.bmp')

# Starry night
def output5():
    for x in range(width):
        for y in range(height):
            if random.random() > 0.995:
                size = random.randrange(0, 3)
                brightness = random.random() / 2 + 0.5
                starColor = color(brightness, brightness, brightness)

                if size == 0:
                    render.glPoint(x, y, starColor)
                elif size == 1:
                    render.glPoint(x, y, starColor)
                    render.glPoint(x + 1, y, starColor)
                    render.glPoint(x, y + 1, starColor)
                    render.glPoint(x + 1, y + 1, starColor)
                elif size == 2:
                    render.glPoint(x, y, starColor)
                    render.glPoint(x, y + 1, starColor)
                    render.glPoint(x + 1, y, starColor)
                    render.glPoint(x, y - 1, starColor)
                    render.glPoint(x - 1, y, starColor)


    render.glFinish('output5.bmp')

def triangle():
    triangle = [
        V2(100, 100), 
        V2(450, 275), 
        V2(250, 500)
    ]
    
    render.glAddVertices(triangle)
    render.glRender()
    render.glFinish('triangle.bmp')

def triangles():
    triangles = [
        V2(100, 100), 
        V2(450, 275), 
        V2(250, 500),
        V2(50, 90),
        V2(300, 100),
        V2(84, 0),
        V2(500, 150),
        V2(10, 330),
        V2(256, 10),
    ]
    
    render.glAddVertices(triangles)
    render.glRender()
    render.glFinish('triangles.bmp')

def noTransformations():
    triangle = [
        V3(0, 0, 0),
        V3(100, 150, 0),
        V3(200, 0, 0)
    ]
    
    render.glAddVertices(triangle)
    render.glModelMatrix()
    render.glRender()
    render.glFinish('noTransformations.bmp')

noTransformations()

def transformations():
    triangle = [
        V3(0, 0, 0),
        V3(100, 150, 0),
        V3(200, 0, 0)
    ]
    
    render.glAddVertices(triangle)
    # render.glModelMatrix()
    render.glModelMatrix(translate=(width/2, height/2, 0), scale=(1, 1, 1))
    render.glRender()
    render.glFinish('transformations.bmp')

transformations()