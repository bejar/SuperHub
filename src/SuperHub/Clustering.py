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

def cluster_colapsed_events(trans, minloc=20, nclust=10, mode='nf', alg='affinity',damping=None):
    """
     Generates a clustering of the users by colapsing the transactions of the user events
     the users have to have at least minloc different locations in their transactions

     :arg   trans: Transaction object
     :arg minloc: Minimum number of locations
     :arg nclust: Number of clusters, for clustering algorithms that need this parameter
     :arg mode:
      * nf = location normalized frequency frequency for the user
      * af = location absolute frequency for the user
      * bin = presence/non presence of the location for the user
      * adding idf used the inverse document frequency

    """
    # Generates a sparse matrix for the transactions and a list of users
    data, users = trans.generate_data_matrix(minloc=minloc, mode=mode)

    print "Clustering Transactions ..."

    if alg == 'affinity':
        ap = AffinityPropagation(damping=damping)
        ap.fit(data)

        ap_labels = ap.labels_
        ap_labels_unique = len(np.unique(ap_labels))
        cclass = np.zeros(ap_labels_unique)

        clusters = {}
        for v in ap_labels:
            cclass[v] += 1

        for v in range(cclass.shape[0]):
            if cclass[v] > 20:
                clusters['c'+str(v)] = []

        for v,u in  zip(ap_labels,users):
            if cclass[v] > 20:
                clusters['c'+str(v)].append(u)

        for c in clusters:
            print c, len(clusters[c])
    return clusters



    # print cclass, np.sum(cclass), len(cclass), reduce(lambda x, y: x + y, [1 for v in cclass if v > 20]), \
    #     reduce(lambda x, y: x + y, [v for v in cclass if v > 20])


    # # Clustering with k-means
    # k_means = KMeans(init='k-means++', n_clusters=nclust, n_init=10, n_jobs=-1)
    #
    # k_means.fit(dataclust)
    #
    # k_means_labels = k_means.labels_
    # k_means_cluster_centers = k_means.cluster_centers_
    # k_means_labels_unique = len(np.unique(k_means_labels))
    # print k_means_labels_unique
    # cclass = np.zeros(k_means_labels_unique)
    # for v in k_means_labels:
    #     #print v
    #     cclass[v] += 1
    # print cclass, np.sum(cclass)
    #
    # for ccenters in k_means_cluster_centers:
    #     print np.count_nonzero(ccenters)





