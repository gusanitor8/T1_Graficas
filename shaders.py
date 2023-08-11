from mathlib import matrix_vector_multiplication, matrix_multiplication
import random
import numpy as np

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

def flatShader(**kwargs):
    dLight = kwargs['dLight']
    normal = kwargs['triangleNormal']
    texture = kwargs['texture']
    texCoords = kwargs['texcoords']

    b = 1.0 
    g = 1.0 
    r = 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])
        b *= textureColor[2]
        g *= textureColor[1] 
        r *= textureColor[0]


    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)

    b *= intensity
    g *= intensity
    r *= intensity
    

    if intensity > 0:
        return r,g,b
    else:
        return (0,0,0)


def colorNoiseShader(**kwargs):
    dLight = kwargs['dLight']
    normal = kwargs['triangleNormal']
    texture = kwargs['texture']
    texCoords = kwargs['texcoords']

    b = 1.0 
    g = 1.0 
    r = 1.0

    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])
        b *= random.randint(0,255)/255
        g *= random.randint(0,255)/255
        r *= random.randint(0,255)/255


    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)

    b *= intensity
    g *= intensity
    r *= intensity
    

    if intensity > 0:
        return r,g,b
    else:
        return (0,0,0)
    

def fragmentShader(**kwargs):
    texcoords = kwargs["texcoords"]
    texture = kwargs["texture"]
    
    if texture != None:
        color = texture.getColor(texcoords[0], texcoords[1])
    else:
        color = (1,1,1)
    
    return color