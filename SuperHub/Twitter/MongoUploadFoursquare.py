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
    if tdata[8] == ' ' or tdata[7] == ' ':
        return None
    else:
       return {
                  'fqurl': tdata[1],
                  'fqtime': tdata[2],
                  'fqid': tdata[3],
                  'gender': tdata[4],
                  'venueid': tdata[5],
                  'venuename': tdata[6],
                  'venuelat': float(tdata[7]),
                  'venuelng': float(tdata[8]),
                  'venuecat': tdata[9],
                  'venuepluralname': tdata[10],
                  'venueshortname': tdata[11],
                  'venueurl': tdata[12]
              }


mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db[mglocal[1]]

cdate = '20150130'

print cdate
#
for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:
    print city
    data = STData(homepath, cityparams[city], 'twitter')
    data.read_py_foursquare_data_full(date=cdate)


    for d in data.dataset:
        #print 'UPD', d[0]
        upd = transform(d)
        if upd is not None:
            col.update({'twid': d[0]}, {'$set': {"foursquare": upd}})
        #else:
        #    print 'vacio'









