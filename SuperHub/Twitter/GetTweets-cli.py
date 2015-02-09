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


from TwitterGetterTimeoutMongo import get_tweets, config_logger
from time import sleep
from Parameters.Pconstants import mongodata
from pymongo import MongoClient

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-c', "--city", help="city to process")
parser.add_argument('-v', "--verbose", help="verbosity", default=0, type=int)
parser.add_argument('-m', "--mongo", help="mongo active", default=0, type=int)
parser.add_argument('-w', "--webservice", help="webservice info", default=0, type=int)

args = parser.parse_args()

if args.city:
    city = args.city
    if args.verbose == 1:
        logger = config_logger(silent=False)
    else:
        logger = config_logger(silent=True)

    if args.mongo == 1:
        mgdb = mongodata.db
        client = MongoClient(mgdb)
        db = client.local
        db.authenticate(mongodata.user, mongodata.passwd)
        col = db['Twitter']
    else:
        col = None

    wsinf = (args.webservice == 1)


    while True:
        get_tweets(city, logger, col, inform=50, wsinf=wsinf)
        sleep(5)
        if args.mongo == 1 and not client.alive():
            col = None
