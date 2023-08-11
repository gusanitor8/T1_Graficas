from gl import Renderer
from Reader import read
import shaders
from math import pi

width = 1000
height = 1000

render = Renderer(width, height)
render.vertexShader = shaders.vertexShader
render.fragmentShader = shaders.colorNoiseShader


def shaderLab():
    filename = "./models/WindMill.obj"
    texturefile = "./models/WindMill.bmp"
    

    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (0, -5, -15),
        rotate=(0, pi/6, -pi/4),
        scale=(1, 1, 1)
    )

    render.glRender()
    render.glFinish("out/shaderLab.bmp")
    
shaderLab()
