import scipy.sparse as sparse

def sparse_matrix(row, col):
    """ Creates sparse matrix with ones on diagonal.
    
    Parameters
    ----------
    row : int, number of rows in the matrix .
    col : int, number of columns in the matrix.
    
    Returns
    -------
    a sparse matrix of size (m x n) whose diagonal is 1 and the rest 0.
    """
    mat = sparse.eye(row, col)
    return(mat)
    