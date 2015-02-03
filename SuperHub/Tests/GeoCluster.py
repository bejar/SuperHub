"""
.. module:: GeoCluster

GeoCluster
*************

:Description: GeoCluster

    

:Authors: bejar
    

:Version: 

:Created on: 04/07/2014 11:59 

"""

__author__ = 'bejar'




from Parameters.Constants import homepath, milanparam
from Analysis import STData
from Analysis.Clustering import cluster_events
from Analysis.Routes import transaction_routes_clustering

def cluster_routes(routes):
    for r in routes:
        param, mxhh, mnhh, alg, radius, mins, size, lpar = r
        data = STData(homepath, param, 'twitter-august')
        data.read_data()
        datahh = data.select_heavy_hitters(mxhh, mnhh)
        clust = cluster_events(datahh, alg=alg, radius=radius, size=size)
        nfile = data.city[2] + '-' + datahh.application + '-routes' + '-nusr' + str(mxhh) + '+' + str(mnhh) \
                + '-crd' + str(radius)
        for supp, timeres in lpar:
            transaction_routes_clustering(datahh, nfile, cluster=clust, supp=supp, timeres=timeres, colapsed=False)

def cluster_geo(routes):
    for r in routes:
        param, mxhh, mnhh, alg, radius, mins, size, sizeprop = r
        data = STData(homepath, param, 'twitter-august')
        data.read_data()
        datahh = data.select_heavy_hitters(mxhh, mnhh)
        cluster_events(datahh, mxhh=mxhh, mnhh=mnhh, alg=alg, radius=radius, mins= mins, size=size, sizeprop=sizeprop)


cluster_geo([
                [milanparam, 0, 20000, 'Leader', 0.001, 50, 50, 10],
                [milanparam, 0, 30000, 'Leader', 0.001, 50, 50, 10],
                [milanparam, 0, 50000, 'Leader', 0.001, 50, 50, 10],
                [milanparam, 0, 70000, 'Leader', 0.001, 50, 50, 10],
                [milanparam, 0, 20000, 'Leader', 0.002, 50, 50, 10],
                [milanparam, 0, 30000, 'Leader', 0.002, 50, 50, 10],
                [milanparam, 0, 50000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 70000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 20000, 'Leader', 0.001, 25, 25, 10],
                [milanparam, 0, 30000, 'Leader', 0.001, 25, 25, 10],
                [milanparam, 0, 50000, 'Leader', 0.001, 25, 25, 10],
                [milanparam, 0, 70000, 'Leader', 0.001, 25, 25, 10],
                [milanparam, 0, 20000, 'Leader', 0.002, 25, 25, 10],
                [milanparam, 0, 30000, 'Leader', 0.002, 25, 25, 10],
                [milanparam, 0, 50000, 'Leader', 0.002, 25, 25, 10],
                [milanparam, 0, 70000, 'Leader', 0.002, 25, 25, 10],
                [milanparam, 0, 20000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 30000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 50000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 70000, 'Leader', 0.003, 50, 50, 10],
                [milanparam, 0, 20000, 'Leader', 0.004, 50, 50, 10],
                [milanparam, 0, 30000, 'Leader', 0.004, 50, 50, 10],
                [milanparam, 0, 50000, 'Leader', 0.004, 50, 50, 10],
                [milanparam, 0, 70000, 'Leader', 0.004, 50, 50, 10],
                [milanparam, 0, 20000, 'Leader', 0.003, 25, 25, 10],
                [milanparam, 0, 30000, 'Leader', 0.003, 25, 25, 10],
                [milanparam, 0, 50000, 'Leader', 0.003, 25, 25, 10],
                [milanparam, 0, 70000, 'Leader', 0.003, 25, 25, 10],
                [milanparam, 0, 20000, 'Leader', 0.004, 25, 25, 10],
                [milanparam, 0, 30000, 'Leader', 0.004, 25, 25, 10],
                [milanparam, 0, 50000, 'Leader', 0.004, 25, 25, 10],
                [milanparam, 0, 70000, 'Leader', 0.004, 25, 25, 10],
                [milanparam, 0, 20000, 'Leader', 0.005, 50, 50, 10],
                [milanparam, 0, 30000, 'Leader', 0.005, 50, 50, 10],
                [milanparam, 0, 50000, 'Leader', 0.005, 50, 50, 10],
                [milanparam, 0, 70000, 'Leader', 0.005, 50, 50, 10],
                [milanparam, 0, 20000, 'Leader', 0.005, 25, 25, 10],
                [milanparam, 0, 30000, 'Leader', 0.005, 25, 25, 10],
                [milanparam, 0, 50000, 'Leader', 0.005, 25, 25, 10],
                [milanparam, 0, 70000, 'Leader', 0.005, 25, 25, 10],


            ])

# cluster_routes([
#                 [milanparam, 50, 30000, 'Leader', 0.001, 100, 100, [(30, 8)]]
#             ])

