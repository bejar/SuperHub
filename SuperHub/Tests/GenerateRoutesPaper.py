# -*- coding: utf-8 -*-
"""

:Description: SuperHub route generation

:Authors:
    bejar

:Version: 1.0

"""
from Parameters.Constants import homepath, cityparams
from Analysis.STData import STData
from Analysis.Routes import transaction_routes_clustering, transaction_routes
# from Clustering import cluster_colapsed_events
# from Transactions import DailyDiscretizedTransactions
from Analysis.Clustering import cluster_events, cluster_cache
from pylab import *
from Analysis.Util import now


def generate_routes(routes):
    for r in routes:
        print str(r)
        param, datafile, mxhh, mnhh, alg, radius, mins, time = r
        data = STData(homepath, param, datafile)
        # data.read_py_data()
        data.read_DB()
        print data.info()
        print 'Data loaded.'
        datahh = data.select_heavy_hitters(mxhh, mnhh)
        if alg == 'Leader':
            clust = cluster_cache(datahh, alg=alg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins)
            if clust is None:
                print 'Computing Clustering'
                clust = cluster_events(datahh, alg=alg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins)
            else:
                print 'Clustering in Cache'
            print 'Clustering Done.'
            now()
            transaction_routes_clustering(datahh, data.city[2] +
                                          data.get_app_name() + '-Leader' + str(radius) + '-nusr' + str(
                mxhh) + '+' + str(mnhh),
                                          cluster=clust, supp=mins, timeres=time)
            now()
        else:
            now()
            transaction_routes(datahh, data.city[2] + data.get_app_name() + '-Grid' + str(radius) + '-nusr' + str(mxhh)
                               + '+' + str(mnhh), scale=radius, supp=mins, timeres=time)
            now()
            print 'Discretized routes.'


def generate_routes_hours(routes, lhours):
    for r in routes:
        print str(r)
        param, datafile, mxhh, mnhh, alg, radius, mins, time = r
        data = STData(homepath, param, datafile)
        data.read_py_data()
        data.info()
        datah = data.select_hours(lhours)
        datah.info()
        datahh = datah.select_heavy_hitters(mxhh, mnhh)
        datahh.info()
        print 'Data loaded.'
        if alg == 'Leader':
            clust = cluster_cache(datahh, alg=alg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins, lhours=lhours)
            if clust is None:
                print 'Computing Clustering'
                clust = cluster_events(datahh, alg=alg, mxhh=mxhh, mnhh=mnhh, radius=radius, size=mins, lhours=lhours)
            else:
                print 'Clustering in Cache'
            print 'Clustering Done.'
            now()
            transaction_routes_clustering(datahh, data.city[2] +
                                          data.get_app_name() + '-H' + str(lhours) + '-Leader' + str(radius)
                                          + '-nusr' + str(mxhh) + '+' + str(mnhh),
                                          cluster=clust, supp=mins, timeres=time)
            now()
        else:
            now()
            transaction_routes(datahh, data.city[2] + data.get_app_name() + '-Grid' + str(radius) + '-nusr' + str(
                mxhh) + '+' + str(mnhh),
                               scale=radius, supp=mins, timeres=time)
            now()
            print 'Discretized routes.'


# Load the data


# generate_routes_hours([
# [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.001, 25, [6,16,18,22]],
#                 [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.003, 25, [6,16,18,22]],
#                 [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.005, 25, [6,16,18,22]]
#                 ], [(22, 24), (0, 6)],
#     )
#
# generate_routes_hours([
#                 [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.001, 25, [6,16,18,22]],
#                 [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.003, 25, [6,16,18,22]],
#                 [bcnparam, 'twitter-august', 50, 70000, 'Leader', 0.005, 25, [6,16,18,22]]
#                 ], [(6, 22)],
#     )

# generate_routes([
#                 [cityparams['bcn'], 'twitter', 50, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 [cityparams['london'], 'twitter', 100, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 [cityparams['paris'], 'twitter', 50, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 [cityparams['rome'], 'twitter', 50, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 [cityparams['berlin'], 'twitter', 50, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 [cityparams['milan'], 'twitter', 50, 70000, 'Leader', 0.005, 20, [6, 18]],
#                 ])

# generate_routes([
#                 [cityparams['bcn'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 [cityparams['london'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 [cityparams['paris'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 [cityparams['rome'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 [cityparams['berlin'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 [cityparams['milan'], 'instagram', 5, 70000, 'Leader', 0.005, 20, [6, 12, 18]],
#                 ])

generate_routes([
    [cityparams['bcn'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]],
    [cityparams['london'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]],
    [cityparams['paris'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]],
    [cityparams['rome'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]],
    [cityparams['berlin'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]],
    [cityparams['milan'], ['twitter', 'instagram'], 50, 70000, 'Leader', 0.005, 30, [6, 18]]
])

print 'Done.'