"""
.. module:: gettweets

gettweets
*************

:Description: gettweets

    

:Authors: bejar
    

:Version: 

:Created on: 01/12/2014 7:38 

"""

__author__ = 'bejar'


from TwitterGetterTimeout import get_tweets, config_logger
from time import sleep
from Parameters.Pconstants import mglocal
from pymongo import MongoClient


# City parameter
city = 'berlin'

logger = config_logger(silent=False)
mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db['Twitter']


while True:
    get_tweets(city, logger, inform=50)
    sleep(10)

