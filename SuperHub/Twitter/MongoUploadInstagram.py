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

from pylab import *
from pymongo import MongoClient

from src.Parameters.Constants import homepath, cityparams
from Analysis import STData
from Parameters.Pconstants import mglocal


def transform(tdata):
   return {
        'lat': tdata[1],
        'lng': tdata[2],
        'igurl': tdata[3],
        'igid': tdata[4],
        'iguname': str(tdata[5])
      }


mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db[mglocal[1]]

cdate = '20150130'


for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:
    print city
    data = STData(homepath, cityparams[city], 'twitter')
    data.read_py_instagram_data_full(date=cdate)


    for d in data.dataset:
        #print 'UPD', d[0]
        upd = transform(d)
        col.update({'twid': d[0]}, {'$set': {"instagram": upd}})









