"""
.. module:: Clustering

Clustering
*************

:Description: Clustering

    Generateq clusterings from  user transactions

:Authors: bejar
    

:Version: 0.1

:Created on: 24/02/2014 9:27 

"""

__author__ = 'bejar'

from Transactions import DailyDiscretizedTransactions
from scipy.sparse import coo_matrix, csr_matrix
import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation
from sklearn.metrics.pairwise import euclidean_distances


def item_to_column(item, scale):
    """
    Transforms an item to a column nuber given the scale of the discretization

    @param item:
    @param scale:
    @return:
    """
    x, y, t = item.split('#')
    return (int(t) * scale * scale) + (int(y) * scale) + int(x)

def generate_data_matrix(trans, scale=100, timeres=4, minloc=20, mode='tf'):
    """
    Generates a sparse data matrix from the transactions
    mode - tf = location frequency for the user
            bin = presence/non presence of the location

    @param trans:
    @param mode:
    @return:
    """
    lcol = []
    lrow = []
    lval = []
    i = 0
    for user in trans:
        #print user
        if len(user) > minloc:
            if mode == 'tf':
                usum = reduce(lambda x, y: x + y, [user[v] for v in user])
                for tr in user:
                    lcol.append(item_to_column(tr, scale))
                    lrow.append(i)
                    lval.append(user[tr]/float(usum))
            elif mode == 'bin':
                for tr in user:
                    lcol.append(item_to_column(tr, scale))
                    lrow.append(i)
                    lval.append(1)

            i += 1

    datamat = coo_matrix((np.array(lval), (np.array(lrow), np.array(lcol))), shape=(i, scale*scale*(24/timeres)))
    return datamat.tocsc()


def cluster_colapsed_events(data, scale=100, timeres=4, minloc=20, nclust=10, mode='tf'):
    """
     Generates a clustering of the users by colapsing the transactions of the user events
     the users have to have at least minloc different locations in their transactions

     mode - tf = location frequency for the user
            bin = presence/non presence of the location
    :param: data:
    :return:
    """
    # Generates the transactions from the user data
    trans = DailyDiscretizedTransactions(data, scale=scale, timeres=timeres)
    usertrans = trans.colapse_count()

    # Generates a sparse matrix for the transactions
    dataclust = generate_data_matrix(usertrans,scale=scale, timeres=timeres, minloc=minloc, mode=mode)

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





