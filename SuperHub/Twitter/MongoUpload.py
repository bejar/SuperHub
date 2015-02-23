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
from pymongo.errors import DuplicateKeyError

from Parameters.Constants import homepath, cityparams
from Analysis.STData import STData
from Parameters.Pconstants import mglocal


def transform(tdata, city):
   return {'city': city,
        'twid': tdata[0].strip(),
        'lat': tdata[1],
        'lng': tdata[2],
        'time': str(tdata[3]),
        'user': tdata[4].strip(),
        'uname': tdata[5].strip(),
        'tweet': tdata[6].decode('ascii', 'ignore').strip()
      }


mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db[mglocal[1]]

cdate = '20150223'


for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:
    print city
    data = STData(homepath, cityparams[city], 'twitter')
    data.read_py_data_full(date=cdate)

    for d in data.dataset:
        #print 'TWID= ', d[0]
        try:
            col.insert(transform(d, city))
        except DuplicateKeyError:
            print 'Duplicate: ',  d[0]

    c = col.find({'city': city})
    print c.count()







