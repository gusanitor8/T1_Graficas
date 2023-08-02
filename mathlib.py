
def matrix_multiplication(matrixA, matrixB):
    rowsA = len(matrixA)
    columnsA = len(matrixA[0])
    rowsB = len(matrixB)
    columnsB = len(matrixB[0])

    if columnsA != rowsB:
        raise ValueError("The number of columns in matrix1 must match the number of rows in matrix2.")
    
    result = [[0 for column in range(columnsB)] for row in range(rowsA)]    
    
    for i in range(rowsA):
        for j in range(columnsB):
            for k in range(columnsA):
                result[i][j] += matrixA[i][k] * matrixB[k][j]
                    
    return(result)

def matrix_vector_multiplication(matrix, vector):
    columnsMatrix = len(matrix[0])
    rowsMatrix = len(matrix)
    rowsVector = len(vector)

    if columnsMatrix != rowsVector:
        raise ValueError("The number of columns in matrix must match the number of rows in vector.")
    
    result = [0 for row in range(rowsMatrix)]

    for i in range(rowsMatrix):
        for j in range(rowsVector):
            result[i] += matrix[i][j] * vector[j]
        
    return(result)

def barycentricCoords(A,B,C,P):
    # areaPBC = abs((P[0] * B[1] + B[0] * C[1] + C[0] * P[1]) - 
    #               (P[1] * B[0] + B[1] * C[0] + C[1] * P[0]))
    
    # areaACP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) - 
    #               (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))
     
    # areaABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) - 
    #               (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    areaPBC = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])

    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])

    areaABC = (B[1] - C[1]) * (A[0] - C[0]) +  (C[0] - B[0]) * (A[1] - C[1])
    
    u = areaPBC / areaABC
    v = areaACP / areaABC
    w = 1 - u - v

    return u,v,w
