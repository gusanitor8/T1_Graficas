
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

matrix = [[2, 3, 1],
 [1, 0, 2]]

vector = [4, 5, 6]

matrix_vector_multiplication(matrix, vector)
