import numpy as np
from sklearn.cluster import KMeans


def myKNN(S, k, sigma=1.0):
    N = len(S)
    A = np.zeros((N, N))

    for i in range(N):
        dist_with_index = zip(S[i], range(N))
        dist_with_index = sorted(dist_with_index, key=lambda x:x[0])
        neighbours_id = [dist_with_index[m][1] for m in range(k+1)] # xi's k nearest neighbours

        for j in neighbours_id: # xj is xi's neighbour
            A[i][j] = np.exp(-S[i][j]/2/sigma/sigma)
            A[j][i] = A[i][j] # mutually
    return A


def calLaplacianMatrix(adjacentMatrix):

    # compute the Degree Matrix: D=sum(A)
    degreeMatrix = np.sum(adjacentMatrix, axis=1)

    # compute the Laplacian Matrix: L=D-A
    laplacianMatrix = np.diag(degreeMatrix) - adjacentMatrix

    # normailze
    # D^(-1/2) L D^(-1/2)
    sqrtDegreeMatrix = np.diag(1.0 / (degreeMatrix ** (0.5)))
    return np.dot(np.dot(sqrtDegreeMatrix, laplacianMatrix), sqrtDegreeMatrix)


def spectral_cluster(dis_matrix, nearest_k, num_k):
    adj_matrix = myKNN(dis_matrix, k=nearest_k, sigma=1.0)
    Laplacian = calLaplacianMatrix(adj_matrix)
    lam, H = np.linalg.eig(Laplacian)
    sp_kmeans = KMeans(n_clusters=num_k).fit(H)
    return sp_kmeans.labels_

