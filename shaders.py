from mathlib import matrix_vector_multiplication, matrix_multiplication, dot_product
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


def toonShader(**kwargs):
    dLight = kwargs['dLight']
    normal = kwargs['triangleNormal']
    texture = kwargs['texture']
    texCoords = kwargs['texcoords']

    # Calculate intensity based on the dot product of light direction and normal
    intensity = dot_product(normal, [-d for d in dLight])
    
    # Apply discrete shading levels for the toon effect
    if intensity > 0.8:
        shading_level = 1.0
    elif intensity > 0.4:
        shading_level = 0.6
    else:
        shading_level = 0.2
    
    # Apply shading level to each color channel
    b = shading_level
    g = shading_level
    r = shading_level

    # Apply texture if available
    if texture is not None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]

    return r, g, b


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

    b = 1.0 
    g = 1.0 
    r = 1.0

    if texture != None:        
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
    
def invertColorShader(**kwargs):
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

        b =  1 - b
        g =  1 - g
        r =  1 - r


    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)

    b *= intensity
    g *= intensity
    r *= intensity
    

    if intensity > 0:
        return r,g,b
    else:
        return (0,0,0)
    

def gradientShader(**kwargs):
    dLight = kwargs['dLight']
    normal = kwargs['triangleNormal']

    c1 = (250, 175, 0)
    c2 = (0, 0, 250)    

    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)

    b = ((c1[2] * intensity + c2[2] * (1 - intensity)))/255
    g = ((c1[1] * intensity + c2[1] * (1 - intensity)))/255
    r = ((c1[0] * intensity + c2[0] * (1 - intensity)))/255    

    if intensity > 0:
        return r,g,b
    else:
        return (0,0,0.98)

def fragmentShader(**kwargs):
    texcoords = kwargs["texcoords"]
    texture = kwargs["texture"]
    
    if texture != None:
        color = texture.getColor(texcoords[0], texcoords[1])
    else:
        color = (0, 0, 250)  
    
    return color