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


def transform(tdata):

   res = {}
   res['city'] = tdata[0].strip()
   res['igid'] = tdata[1].strip()
   res['user'] = tdata[2].strip()
   res['lat'] = float(tdata[3].strip())
   res['lng'] = float(tdata[4].strip())
   res['time'] = tdata[5].strip()
   if tdata[6].strip() != '':
       res['text'] = tdata[6].strip()
   if tdata[7].replace('\n', ' ').strip() != '':
       res['name'] = tdata[7].replace('\n', ' ').strip()


   return res


mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db['Instagram']

cdate = '20150223'


for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:
    print city
    fname = homepath + 'Data-py/instagram/' + city + '-instagram.data'
    rfile = open(fname, 'r')

    for lines in rfile:
        #print 'TWID= ', d[0]
        vals = lines.split(';')
        if len(vals) == 8:
            try:
                col.insert(transform(vals))
                print vals[1]
            except DuplicateKeyError:
                print 'Duplicate: ',  vals[1]
        else:
            print len(vals)

    #c = col.find({'city': city})
    #print c.count()







