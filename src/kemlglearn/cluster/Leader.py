"""
.. module:: Leader

Leader
*************

:Description: Leader Algorithm Clustering

    

:Authors: bejar
    

:Version: 

:Created on: 07/07/2014 8:29 

"""

__author__ = 'bejar'

import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.metrics.pairwise import euclidean_distances


class Leader(BaseEstimator,ClusterMixin,TransformerMixin):
    """Leader Algorithm Clustering

    Paramerets:

    radius: float
        Clustering radius for asigning examples to a cluster

    """
    def __init__(self, radius):
        self.radius = radius
        self.cluster_centers_ = None
        self.labels_ = None
        self.cluser_sizes_ = None

    def fit(self,X):
        """
        Clusters the examples
        :param X:
        :return:
        """
        self.cluster_centers_, self.labels_, self.cluser_sizes_ = self._fit_process(X)

        return self._fit_process(X)

    def predict(self,X):
        """
        Returns the nearest cluster for a data matrix

        @param X:
        @return:
        """
        clasif = []
        for i in range(X.shape[0]):
            ncl, mdist = self._find_nearest_cluster(X[i], self.cluster_centers_)
            if mdist <= self.radius:
                clasif.append(ncl)
            else:
                clasif.append(-1)
        return clasif



    def _fit_process(self, X):
        """
        Clusters incrementally the examples
        :param X:
        :return:
        """
        assignments = []
        scenters = np.zeros((1,X.shape[1]))
        centers = np.zeros((1,X.shape[1]))
        # Initialize with the first example
        scenters[0] = X[0]
        centers[0]  = X[0]
        assignments.append([0])
        csizes=np.array([1])
        #print len(scenters), scenters
        # Cluster the rest of examples
        for i in range(1,X.shape[0]):
            ncl,mdist = self._find_nearest_cluster(X[i], centers)
            #print mdist

            # if distance is less than radius, introduce example in nearest class
            if mdist <= self.radius:
                scenters[ncl] += X[i]
                csizes[ncl] += 1
                centers[ncl] = scenters[ncl]/csizes[ncl]
                assignments[ncl].append(i)
            else: # Create a new cluster
                scenters = np.append(scenters,np.array( [X[i]]), 0)
                centers = np.append(centers,np.array( [X[i]]), 0)
                csizes = np.append(csizes, [1], 0)
                assignments.append([i])

        # centers = np.zeros(scenters.shape)
        # for j in range(scenters.shape[0]):
        #     centers[j] = scenters[j]/csizes[j]
        labels = np.zeros(X.shape[0])
        for l,ej in enumerate(assignments):
            for e in ej:
                labels[e] = l

        return centers, labels, csizes

    def _find_nearest_cluster(self, examp, centers):
        """
        Finds the nearest cluster for an example
        :param examp:
        :param centers:
        :return:
        """

        dist = euclidean_distances(centers,examp)

        pmin = np.argmin(dist)
        vmin = np.min(dist)

        return pmin, vmin
