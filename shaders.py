from mathlib import matrix_vector_multiplication, matrix_multiplication
import random

def vertexShader(vertex, **kwargs):
    
    modelMatrix = kwargs['modelMatrix']
    viewMatrix = kwargs['viewMatrix']
    projectionMatrix = kwargs['projectionMatrix']
    vpMatrix = kwargs['vpMatrix']    

    vt = [
        vertex[0],
        vertex[1],
        vertex[2],
        1
    ]    
    
    # Step 1: Calculate intermediate matrix products
    vp_proj = matrix_multiplication(vpMatrix, projectionMatrix)
    vp_proj_view = matrix_multiplication(vp_proj, viewMatrix)
    final_matrix = matrix_multiplication(vp_proj_view, modelMatrix)

    # Step 2: Multiply the final matrix by vector vt
    vt = matrix_vector_multiplication(final_matrix, vt)

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