# -*- coding: utf-8 -*-
"""

:Description: SuperHub route generation

:Authors:
    bejar

:Version: 1.0

"""
from Parameters.Constants import homepath, bcnparam
from Analysis import STData
from Analysis.Routes import transaction_routes_clustering, transaction_routes
# from Clustering import cluster_colapsed_events
# from Transactions import DailyDiscretizedTransactions
from Analysis.Clustering import cluster_events, cluster_cache
from pylab import *
from Analysis.Util import now


def generate_routes(routes):
    for r in routes:
        param, datafile, mxhh, mnhh, alg, radius, mins, time = r
        data = STData(homepath, param, datafile)
        data.read_data()
        datahh = data.select_heavy_hitters(mxhh, mnhh)
        print 'Data loaded.'
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
                                          data.application + '-Leader' + str(radius) + '-nusr' + str(mxhh) + '+' + str(mnhh),
                                          cluster=clust, supp=mins, timeres=time)
            now()
        else:
            now()
            transaction_routes(datahh, data.city[2] + data.application + '-Grid' + str(radius) + '-nusr' + str(mxhh) + '+' + str(mnhh),
                               scale=radius,supp=mins, timeres=time)
            now()
            print 'Discretized routes.'


def generate_routes_hours(routes,lhours):
    for r in routes:
        param, datafile, mxhh, mnhh, alg, radius, mins, time = r
        data = STData(homepath, param, datafile)
        data.read_data()
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
                clust = cluster_events(datahh, alg=alg,  mxhh=mxhh, mnhh=mnhh,radius=radius, size=mins, lhours=lhours)
            else:
                print 'Clustering in Cache'
            print 'Clustering Done.'
            now()
            transaction_routes_clustering(datahh, data.city[2] +
                                          data.application + '-H' + str(lhours) + '-Leader' + str(radius)
                                          + '-nusr' + str(mxhh) + '+' + str(mnhh),
                                          cluster=clust, supp=mins, timeres=time)
            now()
        else:
            now()
            transaction_routes(datahh, data.city[2] + data.application + '-Grid' + str(radius) + '-nusr' + str(mxhh) + '+' + str(mnhh),
                               scale=radius,supp=mins, timeres=time)
            now()
            print 'Discretized routes.'


# Load the data


generate_routes_hours([
                [bcnparam, 'twitter-august', 75, 70000, 'Leader', 0.001, 25, [5,14,17,22]],
                [bcnparam, 'twitter-august', 75, 70000, 'Leader', 0.002, 25, [5,14,17,22]],
                [bcnparam, 'twitter-august', 75, 70000, 'Leader', 0.003, 25, [5,14,17,22]],
                [bcnparam, 'twitter-august', 75, 70000, 'Leader', 0.004, 25, [5,14,17,22]],
                [bcnparam, 'twitter-august', 75, 70000, 'Leader', 0.005, 25, [5,14,17,22]]
                ], [(22, 24), (0, 6)],
    )



print 'Done.'