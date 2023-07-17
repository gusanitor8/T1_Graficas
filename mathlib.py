def matrix_multiply(matrix1, matrix2):
    # Get the number of rows and columns for each matrix
    rows1 = len(matrix1)
    cols1 = len(matrix1[0])
    rows2 = len(matrix2)
    cols2 = len(matrix2[0])
    
    # Check if the matrices are compatible for multiplication
    if cols1 != rows2:
        raise ValueError("The number of columns in matrix1 must match the number of rows in matrix2.")
    
    # Create an empty result matrix
    result = [[0] * cols2 for _ in range(rows1)]
    
    # Perform matrix multiplication
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    
    return result