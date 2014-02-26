"""
.. module:: Clustering

Clustering
*************

:Description: Clustering

    Generate clusterings from  user transactions

:Authors: bejar
    

:Version: 0.1

:Created on: 24/02/2014 9:27 

"""

__author__ = 'bejar'

import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation
from sklearn.metrics.pairwise import euclidean_distances

def cluster_colapsed_events(trans, minloc=20, nclust=10, mode='tf'):
    """
     Generates a clustering of the users by colapsing the transactions of the user events
     the users have to have at least minloc different locations in their transactions

     Args:
        trans: Transaction object

     KWargs:
     minloc: Minimum number of locations
     nclust: Number of clusters
     mode:
      * tf = location frequency for the user
      * bin = presence/non presence of the location

    """

    # Generates a sparse matrix for the transactions
    dataclust = trans.generate_data_matrix(minloc=minloc, mode=mode)

    # Clustering with k-means
    k_means = KMeans(init='k-means++', n_clusters=nclust, n_init=10, n_jobs=-1)

    k_means.fit(dataclust)

    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = len(np.unique(k_means_labels))
    print k_means_labels_unique
    cclass = np.zeros(k_means_labels_unique)
    for v in k_means_labels:
        #print v
        cclass[v] += 1
    print cclass, np.sum(cclass)

    for ccenters in k_means_cluster_centers:
        print np.count_nonzero(ccenters)





