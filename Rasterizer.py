from gl import Renderer, V2, V3, color
import shaders
import random
from math import pi

width = 1920
height = 1920

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

def renderObj():
    inputFile = './models/skull.obj'
    outputFile = './out/renderObj2.bmp'
    translate = (width/2 ,height/4, 50)
    rotate = (-pi/3, 0, 0)
    scale = (50, 50, 50)

    render.glLoadModel(
        inputFile, 
        translate = translate, 
        scale = scale,
        rotate=rotate)    
    
    render.glRender()
    render.glFinish(outputFile)

renderObj()