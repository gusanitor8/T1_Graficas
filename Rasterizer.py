from gl import Renderer, V2, V3, color
from Reader import read
import shaders
import random
from math import pi

width = 1920
height = 1920

render = Renderer(width, height)
render.vertexShader = shaders.vertexShader
render.fragmentShader = shaders.fragmentShader

def renderObj():
    inputFile = './models/chava.obj'
    outputFile = './out/renderOb3.bmp'
    translate = (width/2 ,0, 50)
    rotate = (0,pi, 0)
    scale = (400, 400, 400)

    render.glLoadModel(
        inputFile, 
        translate = translate, 
        scale = scale,
        rotate=rotate)    
    
    render.glRender()
    render.glFinish(outputFile)

def polyFill():
    FILENAME = "./models/face.txt"
    polyRend = Renderer(width, height)
    points = read(FILENAME)
    polyRend.gldrawPolygon(points)
    polyRend.glFinish("out/polyFill.bmp")     
    

polyFill()