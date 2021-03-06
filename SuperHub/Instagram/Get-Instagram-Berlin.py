"""
.. module:: Get-Instagram-BCN

Get-Instagram-BCN
*************

:Description: Get-Instagram-BCN

    

:Authors: bejar
    

:Version: 

:Created on: 02/02/2015 14:44 

"""

__author__ = 'bejar'

from time import sleep

from pymongo import MongoClient

from InstagramGetter import get_instagram, config_logger
from Parameters.Constants import cityparams
from Parameters.Pconstants import mglocal

# City parameter
city = 'berlin'

logger = config_logger(silent=False)
mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
#db.authenticate(mglocal[2], password=mglocal[3])
col = db['Instagram']
timeout = cityparams[city][4]
additional = 0
## Gets instagram Data at interval times
while True:
    res = get_instagram(city, logger, col, wsinf=True)
    if res == 0:
        sleep(timeout)
    else:
        additional += 240
        sleep(timeout+additional)
