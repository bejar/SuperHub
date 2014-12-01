"""
.. module:: LaplacianScore

LaplacianScore
*************

:Description: LaplacianScore

    Class that computes the laplacian score for a dataset

:Authors: bejar
    

:Version: 

:Created on: 25/11/2014 9:32 

"""

__author__ = 'bejar'

import numpy as np
from sklearn.neighbors import kneighbors_graph, NearestNeighbors

class LaplacianScore():
    """
    Laplacian Score algorithm

    Parameters

        - Number of neighbors to compute the similarity matrix
        - Bandwidth for the gaussian similarity kernel
    """

    _scores = None


    def __init__(self, n_neighbors=5, bandwidth=0.01):
        """
        Initial values of the parameters
        @param n_neighbors:
        @param bandwidth:
        @return:
        """
        self._n_neighbors = n_neighbors
        self._bandwidth = bandwidth

    def fit(self, X):
        """
        Computes the laplacian scores for the dataset

        X is a [n_examples, n_attributes] numpy array
        @return:
        """

        self._scores = self._fit_process(X)

        return self



    def _fit_process(self, X):
        """
        Computes the Laplacian score for the attributes

        ToDo: implementation with sparse matrices

        @param X:
        @return:
        """

        # Similarity matrix
        S = kneighbors_graph(X, n_neighbors=self._n_neighbors,mode='distance')
        S *= S
        S /= self._bandwidth
        S = -S

        ones = np.ones(X.shape[0])

        D = np.diag(np.dot(S,ones))

        L = D - S

        for at in range(X.shape[0]):



