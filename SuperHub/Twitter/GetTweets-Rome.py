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

from time import sleep

from pymongo.mongo_client import MongoClient

from TwitterGetterTimeoutMongo import get_tweets, config_logger
from Parameters.Pconstants import mglocal



# City parameter
city = 'rome'
logger = config_logger(silent=False)
mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
#db.authenticate(mglocal[2], password=mglocal[3])
col = db['Twitter']

while True:
    get_tweets(city, logger, col, inform=50, wsinf=True)
    sleep(10)
    # if not client.alive():
    #     col = None
