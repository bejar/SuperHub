"""
.. module:: test

test
*************

:Description: test

    

:Authors: bejar
    

:Version: 

:Created on: 01/12/2014 11:17 

"""

__author__ = 'bejar'

import time

from TwitterAPI import TwitterAPI

from src.Parameters.Constants import bcnparam
from src.Parameters.Private import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET


api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)

city = bcnparam[2]
initime = int(time.time())

locstr = '%s,%s,%s,%s' % (str(bcnparam[1][2]), str(bcnparam[1][0]), str(bcnparam[1][3]), str(bcnparam[1][1]))

r = api.request('statuses/filter', {'locations': locstr})

i = 0
j = 0
for item in r:
    if 'coordinates' in item:
        print 'C', item['coordinates']
    if 'geo' in item:
        print 'g', item['geo']
    if 'place' in item:
        print 'P', item['place']
    print '---'