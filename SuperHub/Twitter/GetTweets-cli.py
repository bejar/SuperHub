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
import argparse

from pymongo import MongoClient

from TwitterGetterTimeoutMongo import get_tweets, config_logger
from Parameters.Pconstants import mongodata


parser = argparse.ArgumentParser()

parser.add_argument('-c', "--city", help="city to process")
parser.add_argument('-v', "--verbose", help="verbosity", action='store_true', default=False)
parser.add_argument('-m', "--mongo", help="mongo active", action='store_true', default=False)
parser.add_argument('-w', "--webservice", help="webservice info", action='store_true', default=False)

args = parser.parse_args()

print args

if args.city:
    city = args.city
    if args.verbose:
        logger = config_logger(silent=False, file='tw-' + city)
    else:
        logger = config_logger(silent=True, file='tw-' + city)

    if args.mongo:
        mgdb = mongodata.db
        client = MongoClient(mgdb)
        db = client.local
        db.authenticate(mongodata.user, mongodata.passwd)
        col = db['Twitter']
    else:
        col = None

    wsinf = args.webservice

    while True:
        get_tweets(city, logger, col, inform=50, wsinf=wsinf)
        sleep(5)
        # if args.mongo and not client.alive():
        #     col = None
