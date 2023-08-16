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
    filename = "./models/Skull.obj"
    texturefile = "./models/Skull.bmp"
    

    render.glLoadModel(
        filename = filename,
        textureName = texturefile,
        translate = (0, -3, -15),
        rotate=(pi/2, pi, pi),
        scale=(0.3, 0.3, 0.3)
    )

    render.glRender()
    render.glFinish("out/shaderLab3.bmp")
    
shaderLab()
