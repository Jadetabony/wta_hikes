from __future__ import division
import numpy as np

def weighted_cosine_similarity(X, y, weights):
    """Calculates the weighted cosine similarity between two vectors, applying the provided weights.

        X (pandas series): Vector A for cosine similarity calculation
        y (pandas series): Vector B for cosine similarity calculation
        weights (dictionary): Dictionary of weights, keys are the column names as found in X and y. Values are the weights to be applied


        NOTE: weights.values() must sum to one.

        Output: Cosine Similarity between the two vectors, float.
    """
    num = sum([weights[i]*X[i]*y[i] for i in weights.keys()])
    denom = np.sqrt(sum([weights[i]*X[i]**2 for i in weights.keys()]))*np.sqrt(sum([weights[i]*y[i]**2 for i in weights.keys()]))
    return num/denom


def pairwise_cosine_similarity(X, y, weights=None):
    """Compute cosine similarity between samples in X and Y.

        Cosine similarity, or the cosine kernel, computes similarity as the normalized dot product of X and Y:
        K(X, Y) = <X, Y> / (||X||*||Y||)
        Applies weights to the vectors if provided.

        X (pandas DataFrame): Matrix A for cosine similarity calculation
        y (pandas DataFrame): Matrix B for cosine similarity calculation
        Weights (dictionary): Dictionary of weights, keys are the column names as found in X and y. Values are the weights to be applied



        Output: matrix of pairwise similarity comparisons with shape (len(X), len(y))


        NOTE: X and y must be normalized prior to use of this function"""
    final_matrix = np.zeros((len(X), len(y)))

    for i in range(len(X)):
        for j in range(len(y)):
            final_matrix[i][j] = weighted_cosine_similarity(X.ix[i], y.ix[j], weights)

    return final_matrix
