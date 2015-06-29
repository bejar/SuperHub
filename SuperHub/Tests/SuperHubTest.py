# -*- coding: utf-8 -*-
"""

:Description: SuperHub statistics and route generation

:Authors:
    bejar

:Version: 1.0

"""
import time

import pylab as pl
from pylab import *
from pymongo import MongoClient

from Parameters.Constants import mgpass, mguser, homepath, bcnparam
from STData import STData
from Routes import transaction_routes_many
from Analysis.Clustering import cluster_colapsed_events
from Transactions import DailyDiscretizedTransactions


def visual(X):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    pl.scatter(X[:, 1], X[:, 2], zs=X[:, 0], s=25)

    pl.show()


def compute_transactions_routes(data):
    """
    Computes frequent routes from the frequent transactions
    @param data:
    @return:
    """
    transaction_routes_many(data, lhh=[(0, 40000)], lscale=[150], supp=10, ltimeres=[8])


def compute_transactions_clusters(data, alg='affinity', mode='binidf', scale=100, timeres=4, nclust=10,
                                  minloc=20, damping=0.5):
    """
    Computer the clustering of the user colapsed transactions
    @param data:
    @return:
    """

    # Select Heavy Hitters
    datahh = data.select_heavy_hitters(100, 25000)

    trans = DailyDiscretizedTransactions(datahh, scale=scale, timeres=timeres)
    ### Clustering
    cls = cluster_colapsed_events(trans, minloc=minloc, mode=mode, alg=alg, damping=damping, nclust=nclust)
    lusers = []
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())

    for c in cls:
        dataclus = data.select_data_users(cls[c])
        dataclus.plot_events_grid(scale=scale,
                                  dataname=mode + '-' + alg + '-' + str(minloc) + '-ts' + today + '-cluster-' + c,
                                  distrib=True, timeres=0)


def ReviewUsers(cityparam, application, lusers, intinit, intend=None):
    """

    :param: application:
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]

    if intend is None:
        intend = int(time.time())
    print intend

    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    dusers = {}


    # names= db.collection_names()
    col = db['sndata']
    # c = col.find_one({'app': application,
    #                   'lat': {'$gt': minLat, '$lt': maxLat},
    #                   'lng': {'$gt': minLon, '$lt': maxLon},
    #                  }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
    c = col.find({'app': application,
                  'lat': {'$gt': minLat, '$lt': maxLat},
                  'lng': {'$gt': minLon, '$lt': maxLon},
                  'interval': {'$gt': intinit, '$lt': intend}
                  }, timeout=False)

    for t in c:
        #        stime=time.localtime(t['interval'])
        #        evtime=time.strftime('%Y%m%d',stime)
        #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
        #  rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])
        # +',\''+str(t['text']).strip().replace('\n','')+'\'\n')
        if t['user'] in lusers:
            #lusers.remove(t['user'])
            print t['user'],
            print t['text'],
            v = t['user-twitter']
            print v['name'], v['screen_name']
            if t['user'] not in dusers:
                dusers[t['user']] = (v['name'], v['screen_name'], t['text'])

    return dusers

# Load the data from the DB to a file
# getApplicationData('twitter')
#getApplicationData('instagram')
#getLApplicationData(['twitter','instagram'])

# What data?
# application = 'twitter+instagram' aQZ
#
# twig = TIJoinData(homepath,application)
# twig.read_data()
# twig.generate_correspondences()
# print len(twig.correspondence)

data = STData(homepath, bcnparam, 'twitter-august')
data.read_data()
users = data.compute_heavy_hitters(0, 50)
print 'Done'
us = ReviewUsers(bcnparam, 'twitter', users, 1405940998)
print '.....................'
for u in us:
    print us[u]

# c= getApplicationDataOneUser(bcnparam, 'twitter', '495009558')
# print c['user'],
# print c['text'],
# v = c['user-twitter']
# print v['name'], v['screen_name']


# data = STData(homepath, bcnparam, 'twitter-august')
# data.read_data()
# data.info()
# datah = data.select_hours([(6, 22)])
# datah.info()
# datahh = datah.select_heavy_hitters(50, 50000)
# datahh.info()

#datahh.grid_events(60,threshold=25,distrib=False)

# data_histograms(data,lhh=[(0, 20000)])
# user_events_histogram(data,scale=300,timeres=4)

#compute_transactions_routes(data)
# compute_transactions_clusters(data, alg='affinity', mode='bin', scale=150, timeres=8, nclust=30,
#                               minloc=20, damping=0.5)

# udict= data.generate_user_dict()
# print len(udict)
# igcnt=0
# for u in twig.correspondence:
#     user = twig.correspondence[u]
#     if user in udict:
#         igcnt += udict[user]
#
# print igcnt



# for u in udict:
#     print u, udict[u]






# Load the data from the file


### Dimensionality reduction

#pca = KernelPCA(n_components=3, kernel='cosine')
#lle = LocallyLinearEmbedding(n_components=3, method='modified')

# iso = Isomap(n_components=4, n_neighbors=20)
# x = iso.fit_transform(data.toarray())
#
# visual(x)


#
# k_means = KMeans(init='k-means++', n_clusters=15, n_init=10, n_jobs=-1)
#
# k_means.fit(data)
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



### Do things with the data

#plot_accumulated_events(data,distrib=False,scale=300)
#accumulatedEvents('twitter',5,3000,distrib=False,scale=200)
#event_histograms('twitter',5,5000)
#daily_histogram('twitterinstagram',5,5000)
#hourly_histogram('twitterinstagram',5,5000)
#pp = pprint.PrettyPrinter(indent=4)

#data_histograms('instagram',lhh=[(0, 20000)])
#data_histograms('twitter',lhh=[(0,20000)])
#getApplicationData('twitter')
#hourly_histogram('instagram',5,4000)

#saveDailyTransactions('hh','twitter',5,8000,scale=200)

#transferApplicationData('twitter')


#transaction_routes_many(data,lhh=[(100, 20000)], lscale=[100,200], supp=30, ltimeres=[4])

#user_events_histogram('twitter',100,20000,300,4)
#user_events_histogram('instagram',100,20000,300,4)

#montly_histogram('twitter', 0, 20000)

#user_events_histogram(data)
print 'Done.'