"""
.. module:: TestMongo

TestMongo
*************

:Description: TestMongo

    

:Authors: bejar
    

:Version: 

:Created on: 16/01/2015 11:01 

"""

__author__ = 'bejar'


from Constants import homepath, cityparams
from STData import STData
from Routes import transaction_routes_many
from Clustering import cluster_colapsed_events
from Transactions import DailyDiscretizedTransactions
from Descriptive import data_histograms, user_events_histogram
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.decomposition import PCA, KernelPCA
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from sklearn.manifold import LocallyLinearEmbedding, Isomap
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation
from sklearn.mixture import DPGMM
from Util import strip_nl
from DB import getApplicationData
from TIJoinData import TIJoinData
import time
from Transactions import DailyTransactions, DailyDiscretizedTransactions
from pymongo import MongoClient
import pprint
from Pconstants import mglocal

def transform(tdata, city):
   return {'city': city,
        'twid': tdata[0],
        'lat': tdata[1],
        'lng': tdata[2],
        'time': str(tdata[3]),
        'user': tdata[4],
        'uname': tdata[5],
        'tweet': tdata[6]
      }


mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db[mglocal[1]]

cdate = '20141212'


for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:
    print city
    data = STData(homepath, cityparams[city], 'twitter')
    data.read_py_data_full(date=cdate)

    for d in data.dataset:
        #print d
        col.insert(transform(d, city))
    c = col.find({'city': city})
    print c.count()







