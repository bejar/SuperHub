"""
.. module:: GenerateClustersPaper.py

GenerateClustersPaper.py
*************

:Description: GenerateClustersPaper.py

    

:Authors: bejar
    

:Version: 

:Created on: 08/10/2014 9:58 

"""

__author__ = 'bejar'

import time

from pylab import *

from Parameters.Constants import homepath, bcnparam
from Analysis.STData import STData
from Analysis.Transactions import DailyDiscretizedTransactions, DailyClusteredTransactions
from Analysis.Clustering import cluster_events, cluster_cache, cluster_colapsed_events, cluster_colapsed_events_simple
from Analysis.Util import now
from Analysis import TimeDiscretizer


def compute_transactions_clusters(r, alg=['affinity'], mode='binidf', nclust=10,
                                  minloc=20, damping=0.5, output='map', minsize=20):
    """
    Computer the clustering of the user colapsed transactions

    @param data:
    @param output: 'map', 'sizes', 'labels'
    @return:
    """
    param, datafile, mxhh, mnhh, calg, radius, mins, timedis = r
    data = STData(homepath, param, datafile)
    data.read_data()
    datahh = data.select_heavy_hitters(mxhh, mnhh)
    print 'Data loaded.'



    if calg == 'Leader':
        clust = cluster_cache(datahh, alg=calg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins)
        if clust is None:
            print 'Computing Clustering'
            clust = cluster_events(datahh, alg=calg,  mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins)
        else:
            print 'Clustering in Cache'
        print 'Clustering Done.'
        now()
        trans = DailyClusteredTransactions(datahh, cluster=clust, timeres=TimeDiscretizer(timedis))
        # Generates a sparse matrix for the transactions and a list of users
        datamat, users = trans.generate_data_matrix(minloc=minloc, mode=mode)

        now()

        for calg in alg:
        ### Clustering
            if calg == 'affinity':
                labncls = '-damp' + str(damping)
            else:
                labncls = '-nclust' + str(nclust)

            cls = cluster_colapsed_events(datamat, users, minloc=minloc, mode=mode,
                                          alg=calg, damping=damping, nclust=nclust)
            lusers = []
            today = time.strftime('%Y%m%d%H%M%S', time.localtime())


            if output == 'sizes' or output == 'all':
                rfile = open(homepath + 'Results/' + data.city[2] + data.application
                             + mode + '-sizes-' + calg + '-minloc' + str(minloc) + '-minsize' + str(minsize)
                             + '-timed' + str(TimeDiscretizer(timedis).intervals)
                             + labncls
                             + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-r' + str(radius)
                             + '.csv', 'w')
                for c in cls:
                    rfile.write(str(c)+','+str(len(cls[c]))+'\n')
            if output == 'labels' or output == 'all':
                rfile = open(homepath + 'Results/' + data.city[2] + data.application
                             + mode + '-labels-' + calg + '-minloc' + str(minloc) + '-minsize' + str(minsize)
                             + '-timed' + str(TimeDiscretizer(timedis).intervals)
                             + labncls
                             + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-r' + str(radius)
                             + '.csv', 'w')
                for c in cls:
                    for ex in cls[c]:
                        rfile.write(str(c)+', '+str(ex)+'\n')
            if output == 'map' or output == 'all':
                for c in cls:
                    if len(cls[c]) > minsize:
                        print 'cluster ' + c
                        dataclus = data.select_data_users(cls[c])
                        dataclus.plot_events_cluster(cluster=clust, dataname=mode+'-'+calg+'-'+str(minloc)+'-ts' + today
                                                     + labncls + '-cluster-' + c + '-csize' + str(len(cls[c]))
                                                     + '-timed' + str(TimeDiscretizer(timedis).intervals),
                                                     distrib=True, timeres=None) # TimeDiscretizer(timedis))

    else:
        now()
        trans = DailyDiscretizedTransactions(datahh, scale=radius, timeres=TimeDiscretizer(timedis))
        now()

        for calg in alg:
        ### Clustering
            cls = cluster_colapsed_events(trans, minloc=minloc, mode=mode, alg=calg, damping=damping, nclust=nclust)
            lusers = []
            today = time.strftime('%Y%m%d%H%M%S', time.localtime())
            fname = mode+'-'+calg+'-'

            if calg == 'kmeans':
                fname += '-mxcl' + str(nclust)
            elif calg == 'affinity':
                fname += '-damp' + str(damping)
            if calg == 'affinity':
                labncls = '-damp' + str(damping)
            else:
                labncls = '-nclust' + str(nclust)

            fname += '-minloc' + str(minloc) + '-ts' + today

            if output == 'sizes' or output == 'all':
                rfile = open(homepath + 'Results/' + data.city[2] + data.application
                             + mode+'sizes-'+ calg + '-minloc' + str(minloc)+'-minsize' + str(minsize)
                             + '-timed' + str(TimeDiscretizer(timedis).intervals)
                             + labncls
                             + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-s' + str(radius)
                             + '.csv', 'w')
                for c in cls:
                    rfile.write(str(c)+','+str(len(cls[c]))+'\n')
            if output == 'labels' or output == 'all':
                rfile = open(homepath + 'Results/' + data.city[2] + data.application
                             + mode+'-labels-'+ calg + '-minloc' + str(minloc)+'-minsize' + str(minsize)
                             + '-timed' + str(TimeDiscretizer(timedis).intervals)
                             + labncls
                             + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-s' + str(radius)
                             + '.csv', 'w')
                for c in cls:
                    for ex in cls:
                        rfile.write(str(c)+','+str(ex)+'\n')
            if output == 'map' or output == 'all':
                for c in cls:
                    print 'cluster ' + c
                    dataclus = data.select_data_users(cls[c])
                    dataclus.plot_events_grid(scale=radius, dataname= fname + labncls + '-cluster-'
                                              + c + '-csize' + str(len(cls[c]))
                                              + '-timed' + str(TimeDiscretizer(timedis).intervals),
                                              distrib=True, timeres=0)


def explore_number_of_clusters(r, alg='affinity', mode='binidf', scale=100, nclust=10,
                               minloc=20, damping=0.5):

    param, datafile, mxhh, mnhh, calg, radius, mins, timedis = r
    data = STData(homepath, param, datafile)
    data.read_data()
    datahh = data.select_heavy_hitters(mxhh, mnhh)
    print 'Data loaded.'


    if calg == 'Leader':
        clust = cluster_cache(datahh, alg=calg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins)
        if clust is None:
            print 'Computing Clustering'
            clust = cluster_events(datahh, alg=calg,  mxhh=mxhh, mnhh=mnhh,radius=radius, size=mins)
        else:
            print 'Clustering in Cache'
        print 'Clustering Done.'
        now()
        trans = DailyClusteredTransactions(datahh, cluster=clust, timeres= TimeDiscretizer(timedis))
        now()

        ### Clustering
        lvals = cluster_colapsed_events_simple(trans, minloc=minloc, mode=mode, alg=alg, damping=damping, nclust=nclust)
        for v in  lvals:
            print v

    else:
        now()
        trans = DailyDiscretizedTransactions(datahh, scale=scale, timeres=TimeDiscretizer(timedis))
        now()

        ### Clustering
        lvals = cluster_colapsed_events_simple(trans, minloc=minloc, mode=mode, alg=alg, damping=damping, nclust=nclust)
        for v in lvals:
            print v


# for i in [0.001, 0.0025, 0.005]:
#     for j in [[6, 18], [6, 16, 22], [6, 16, 18, 22]]:
#         compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', i, 25, j],
#                                       alg=['kmeans', 'affinity', 'spectral'], mode='bin', nclust=60,
#                                       minloc=20, damping=0.999, minsize=20, output='sizes')

for i in [0.001, 0.0025, 0.005]:
    for j in [[6, 18], [6, 16, 22], [6, 16, 18, 22]]:
        compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', i, 25, j],
                                      alg=['kmeans', 'affinity', 'spectral'], mode='bin', nclust=100,
                                      minloc=20, damping=0.5, minsize=20, output='all')



# for i in [0.001, 0.0025, 0.005]:
#     for j in [[6, 18], [6, 16, 22], [6, 16, 18, 22]]:
#         for k in ['kmeans', 'affinity', 'spectral']:
#             compute_transactions_clusters([bcnparam, 'instagram-september', 0, 70000, 'Leader', i, 25, j],
#                                           alg=k, mode='bin', nclust=60,
#                                           minloc=25, damping=0.5, minsize=0, output='sizes')

# for i in [0.001, 0.0025, 0.005]:
#     for j in [[6, 18], [6, 16, 22], [6, 16, 18, 22]]:
#         for k in ['affinity']:
#             compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', i, 25, j],
#                                           alg=k, mode='bin', nclust=60,
#                                           minloc=20, damping=0.999, minsize=0, output='labels')

# for k in ['kmeans', 'affinity', 'spectral']:
#     compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', 0.005, 25, [6, 18]],
#                                   alg=k, mode='bin', nclust=60,
#                                   minloc=20, damping=0.5, minsize=0, output='labels')


# compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', 0.005, 25, [6, 16, 18, 22]],
#                               alg='affinity', mode='bin', nclust=60,
#                               minloc=20, damping=0.999, minsize=0, output='sizes')


# compute_transactions_clusters([bcnparam, 'twitter-september', 50, 70000, 'Leader', 0.005, 25, [6, 18]],
#                               alg='affinity', mode='bin', nclust=100,
#                               minloc=20, damping=0.999, minsize=0, simple=True)
#

# compute_transactions_clusters([milanparam, 'twitter-august', 0, 70000, 'Leader', 0.0025, 25, [6, 18]],
#                               alg='kmeans', mode='bin', scale=60, nclust=30,
#                               minloc=15, damping=0.999)

# explore_number_of_clusters([bcnparam, 'instagram-august', 0, 70000, 'Leader', 0.003, 25, [6, 18]],
#                            alg='kmeans', mode='bin', scale=60, nclust=(300,350),
#                            minloc=20, damping=0.98)
