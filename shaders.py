from mathlib import matrix_vector_multiplication
import random
import numpy as np

def vertexShader(vertex, **kwargs):
    
    modelMatrix = kwargs['modelMatrix']

    vt = [
        vertex[0],
        vertex[1],
        vertex[2],
        1
    ]
    # vt = m.matrix_multiply([vt], modelMatrix)
    # vt = vt[0]

    vt = np.array(vt)
    
    #modelMatrix = np.array(modelMatrix)

    vt =  matrix_vector_multiplication(modelMatrix, vt)

    vt = [vt[0] / vt[3], 
          vt[1] / vt[3], 
          vt[2] / vt[3]
    ]

    return vt


def fragmentShader(**kwargs):
    texcoords = kwargs["texcoords"]
    texture = kwargs["texture"]
    
    if texture != None:
        color = texture.getColor(texcoords[0], texcoords[1])
    else:
        color = (1,1,1)
    
    return color