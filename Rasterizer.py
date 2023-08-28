from gl import Renderer
from Reader import read
import shaders
from math import pi

width = 1000
height = 1000
backgroundImg = "models/farm.bmp"

render = Renderer(width, height)
render.glBackgroundTexture(backgroundImg)
render.glClearBackground()

render.vertexShader = shaders.vertexShader



def project():
    #modelo 1 TORO
    filename = "./models/toro/toro.obj"
    texturefile = "./models/toro/toro.bmp"    
    
    render.fragmentShader = shaders.flatShader
    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (-5, -15, -40),
        rotate=(pi, pi, pi),
        scale=(1, 1, 1)
    )
    render.glRender()

    #modelo 2 PATO
    filename = "./models/pato/pato.obj"
    texturefile = "./models/pato/pato.bmp"    

    render.fragmentShader = shaders.flatShader
    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (0, -8, -15),
        rotate=(pi/2, pi, pi),
        scale=(0.03, 0.03, 0.03)
    )
    render.glRender()

    #modelo 3 GATO
    filename = "./models/cat/cat.obj"
    texturefile = "./models/cat/cat.bmp"    

    render.fragmentShader = shaders.flatShader
    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (-3, -8, -15),
        rotate=(pi/2, pi, pi),
        scale=(0.07, 0.07, 0.07)
    )
    render.glRender()

    #modelo 4 wind mill
    filename = "./models/WindMill/WindMill.obj"
    texturefile = "./models/WindMill/WindMill.bmp"    

    render.fragmentShader = shaders.flatShader
    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (-3, -8, -60),
        rotate=(pi, 3.3, pi),
        scale=(1, 1, 1)
    )
    render.glRender()

    
    render.glFinish("out/shaderLab3.bmp")
    
project()
