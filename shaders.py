from mathlib import matrix_multiply
import mathlib as m
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

    vt =  modelMatrix @ vt
    vt = vt.tolist()[0]

    vt = [vt[0] / vt[3], 
          vt[1] / vt[3], 
          vt[2] / vt[3]
    ]

    return vt
    # transformedVertex = vertex
    # return transformedVertex

def fragmentShader(**kwargs):
    color = (1, 1, 1)
    return color