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
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter
from cluster.Leader import Leader
from Util import now
from Constants import homepath
import time
from numpy import savetxt
import folium
from geojson import LineString, GeometryCollection, FeatureCollection, Feature
import geojson
import os.path
import pickle

circlesize = 15000


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

        for v,u in zip(ap_labels,users):
            if cclass[v] > 20:
                clusters['c'+str(v)].append(u)

        for c in clusters:
            print c, len(clusters[c])
    if alg == 'kmeans':
        k_means = KMeans(init='k-means++', n_clusters=nclust, n_init=10, n_jobs=-1)
        k_means.fit(data)
        k_means_labels = k_means.labels_
        #k_means_cluster_centers = k_means.cluster_centers_
        k_means_labels_unique = len(np.unique(k_means_labels))
        cclass = np.zeros(k_means_labels_unique)
        clusters = {}

        for v in k_means_labels:
            cclass[v] += 1
        for v in range(cclass.shape[0]):
            if cclass[v] > 20:
                clusters['c'+str(v)] = []

        for v,u in zip(k_means_labels,users):
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


def cluster_cache(data, mxhh=0, mnhh=0, radius=0.01, mins=100, size=100, alg='Leader'):
    if alg == 'Leader':
        nfile = homepath + 'Clusters/' + data.city[2] + data.application + '-' + 'nusr' + str(mxhh) + '+' + str(mnhh) \
            + '-' + 'Leader-crd' + str(radius) + '-mex' + str(size)+'.pkl'
    elif alg == 'DBSCAN':
        nfile = homepath + 'Clusters/' + data.city[2] + data.application + '-' + 'nusr' + str(mxhh) + '+' + str(mnhh) \
            + '-' + 'DBSCAN-crd' + str(radius) + '-mins' + str(mins) + '-mex' + str(size) + '.pkl'
    if os.path.isfile(nfile):
        pfile = open(nfile,'r')
        return pickle.load(pfile)
    else:
        return None


def cluster_events(data, nclust=10, mxhh=0, mnhh=0, radius=0.01, mins=100, size=100, alg='Leader', sizeprop=0):
    """
    Cluster geographical events and returns the clusters

    @param nclust:
    @return:
    """
    coord = data.getDataCoordinates()

    if alg == 'Leader':
        dbs = Leader(radius=radius)
    elif alg == 'DBSCAN':
        dbs = DBSCAN(eps=radius, min_samples=mins, algorithm='kd_tree')
    else:
        dbs = None
    now()
    dbs.fit(coord)
    now()

    if alg == 'Leader':
        sizes = dbs.cluster_sizes_
        plot_clusters(data, dbs.cluster_centers_[sizes > size],
                      sizes[sizes > size],
                      sizeprop=250,
                      dataname='leader-crd'+ str(radius) + '-mex' + str(size))
        nfile = homepath + 'Results/' + data.city[2] + data.application + '-' + 'nusr' + str(mxhh) + '+' + str(mnhh) \
                + '-' + 'Leader-crd' + str(radius) + '-mex' + str(size)+'.csv'
        savetxt(nfile, dbs.cluster_centers_[sizes > size],delimiter=';')
        nfile = homepath + 'Clusters/' + data.city[2] + data.application + '-' + 'nusr' + str(mxhh) + '+' + str(mnhh) \
                + '-' + 'Leader-crd' + str(radius) + '-mex' + str(size)+'.pkl'
        pkfile = open(nfile, 'w')
        pickle.dump(dbs, pkfile)
        pkfile.close()
    elif alg == 'DBSCAN':
        labset = set(dbs.labels_)
        if -1 in labset:
            dim = len(labset) -1
        else:
            dim = len(set)
        centers = np.zeros((dim,2))
        sizes = np.zeros(dim)
        dataset = data.dataset
        clres = np.zeros((dataset.shape[0],3))
        for i in range(dataset.shape[0]):
            clres[i][0] = dataset[i][0]
            clres[i][1] = dataset[i][1]
            clres[i][2] = dbs.labels_[i]
            if dbs.labels_[i] != -1:
                sizes[int(dbs.labels_[i])] += 1
                centers[int(dbs.labels_[i])][0] += dataset[i][0]
                centers[int(dbs.labels_[i])][1] += dataset[i][1]

        for i in range(sizes.shape[0]):
            centers[i][0] /= sizes[i]
            centers[i][1] /= sizes[i]
            print sizes[i]
        nfile = homepath + 'Results/' + data.city[2] + data.application + '-'
        savetxt(nfile + 'DBSCAN-crd' +str(radius) + '-mins'+ str(mins) + '-mex'+ str(size) + '.csv', clres, delimiter=';')
        plot_clusters(data, centers[sizes > size], sizes[sizes > size], dataname='dbscan-crd'+str(radius)
                      + '-mins'+ str(mins) + '-mex'+str(size), sizeprop=sizeprop)

    return dbs


def plot_clusters(data, centroids, csizes, sizeprop=1000, dataname=''):
    """
    Generates an scale x scale plot of the events
    Every event is represented by a point in the graph
    the ouput is an html file that uses open street maps

    :param string dataname: Name to append to the filename
    """

    print 'Generating the events plot ...'

    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    minLat, maxLat, minLon, maxLon = data.city[1]
    mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1400, height=1400)

    # if distrib:
    #     cont = cont / np.max(cont)
    #     plt.imshow(cont, interpolation='bicubic', cmap=cm.gist_yarg)
    #     for i in range(cont.shape[0]):
    #         for j in range(cont.shape[1]):
    #             if cont[i, j] != 0:
    #                 mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
    #                                     radius=cont[i,j]*(circlesize/scale),
    #                                     line_color='#FF0000',
    #                                     fill_color='#110000')
    maxsize = np.max(csizes)/sizeprop

    for i in range(centroids.shape[0]):
            if sizeprop != 0:
                plotsize = csizes[i]/maxsize
            else:
                plotsize = 10
            mymap.circle_marker(location=[centroids[i][0], centroids[i][1]],
                                radius=plotsize,
                                line_color='#FF0000',
                                fill_color='#110000')

    nfile = data.application + '-' + dataname

    mymap.create_map(path=homepath + 'Results/' + data.city[2] + nfile + '-ts' + today + '.html')

