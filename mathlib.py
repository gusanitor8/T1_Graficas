PI = 3.141592653589

def dot_product(vector1, vector2):
    return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

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
    areaPBC = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])

    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])

    areaABC = (B[1] - C[1]) * (A[0] - C[0]) +  (C[0] - B[0]) * (A[1] - C[1])
    
    try:
        u = areaPBC / areaABC
        v = areaACP / areaABC
        w = 1 - u - v
    except Exception:
        u = 0
        v = 0
        w = 1
        

    return u,v,w

def makeIdentityMatrix(n):
    identityMatrix = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        identityMatrix[i][i] = 1
    return identityMatrix

def inverseMatrix(matrix):
    row_number = len(matrix)
    col_number = len(matrix[0])
    id_matrix = makeIdentityMatrix(row_number)

    for i in range(row_number):
        for j in range(col_number):
            matrix[i].append(id_matrix[i][j])
    
    result = gauss_jordan(matrix)
    return result


def gauss_jordan(matrix):
    n = len(matrix)
    
    for i in range(n):
        # Partial pivoting
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Normalize the current row
        pivot = matrix[i][i]
        for j in range(i, n * 2):
            matrix[i][j] /= pivot

        # Eliminate other rows
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, n * 2):
                    matrix[j][k] -= factor * matrix[i][k]

    # Extract the inverse matrix from the augmented matrix
    result = [row[n:] for row in matrix]
    
    return result