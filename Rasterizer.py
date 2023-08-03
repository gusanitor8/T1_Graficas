from gl import Renderer, V2, V3, color
from Reader import read
import shaders
import random
from math import pi

width = 1000
height = 1000

render = Renderer(width, height)
render.vertexShader = shaders.vertexShader
render.fragmentShader = shaders.fragmentShader

def doTriangle():
    triangle = [(130,50), (200, 100), (50, 250)]
    render.glTriangle(triangle[0], triangle[1], triangle[2])
    render.glFinish('out/triangle.bmp')

def doBcTriangle():
    triangle = [(130,50), (200, 100), (50, 250)]
    render.glTriangle_bc(triangle[0], triangle[1], triangle[2])
    render.glTriangle(triangle[0], triangle[1], triangle[2])
    render.glFinish('out/triangle.bmp')

def renderObj():
    inputFile = './models/Knife.obj'
    outputFile = './out/renderOb3.bmp'
    textureFile = './models/Albedo.bmp'
    translate = (width/2 , height/2, 0)
    rotate = (0, 0, 0)
    scale = (200, 200, 200)

    render.glLoadModel(
        inputFile, 
        translate = translate, 
        scale = scale,
        rotate=rotate,
        textureName=textureFile)    
    
    render.glRender()
    render.glFinish(outputFile)

def R2Textures():
    inputFile = './models/WindMill.obj'
    outputFile = './out/renderOb3.bmp'
    textureFile = './models/WindMill.bmp'


    #first model
    translate0 = (width*(1/4) , height*(1/2), 0)
    rotate0 = (0, pi/4, 0)
    scale = (30, 30, 30)

    #second model
    translate1 = (width*(3/4) , height*(1/2), 0)
    rotate1 = (0, 0, 0)    

    #third model
    translate2 = (width*(1/4) , height*(1/6), 0)
    rotate2 = (0, pi, 0)    

    #fourth model
    translate3 = (width*(3/4) , height*(1/6), 0)
    rotate3 = (-pi/2.4, 0, 0)

    render.glLoadModel(
        inputFile, 
        translate = translate0, 
        scale = scale,
        rotate=rotate0,
        textureName=textureFile)    
    
    render.glLoadModel(
        inputFile, 
        translate = translate1, 
        scale = scale,
        rotate=rotate1,
        textureName=textureFile)  
    
    render.glLoadModel(
        inputFile, 
        translate = translate2, 
        scale = scale,
        rotate=rotate2,
        textureName=textureFile)  
    
    render.glLoadModel(
        inputFile, 
        translate = translate3, 
        scale = scale,
        rotate=rotate3,
        textureName=textureFile)  
    
    render.glRender()
    render.glFinish(outputFile)

def polyFill():
    FILENAME = "./models/face.txt"
    FILENAME2 = "./models/face2.txt"
    FILENAME3 = "./models/face3.txt"
    FILENAME4 = "./models/face4.txt"
    FILENAME5 = "./models/face5.txt"

    polyRend = Renderer(width, height)
    points = read(FILENAME)
    points2 = read(FILENAME2)
    points3 = read(FILENAME3)
    points4 = read(FILENAME4)
    points5 = read(FILENAME5)

    color1 = color(0, 0, 0)
    polyRend.gldrawPolygon(points)
    polyRend.gldrawPolygon(points2)
    polyRend.gldrawPolygon(points3)
    polyRend.gldrawPolygon(points4)
    polyRend.gldrawPolygon(points5, clr= color1)
    polyRend.glFinish("out/polyFill2.bmp")  

R2Textures()
