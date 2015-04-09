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
import argparse

from pymongo import MongoClient

from InstagramGetter import get_instagram, config_logger
from Parameters.Constants import cityparams
from Parameters.Pconstants import mongodata

parser = argparse.ArgumentParser()

parser.add_argument('-c', "--city", help="city to process")
parser.add_argument('-v', "--verbose", help="verbosity", action='store_true', default=False)
parser.add_argument('-m', "--mongo", help="mongo active", action='store_true', default=False)
parser.add_argument('-w', "--webservice", help="webservice info", action='store_true', default=False)

args = parser.parse_args()

# City parameter

if args.city:
    city = args.city
    if args.verbose == 1:
        logger = config_logger(silent=False, file='ig-' + city)
    else:
        logger = config_logger(silent=True, file='ig-' + city)

    if args.mongo == 1:
        mgdb = mongodata.db
        client = MongoClient(mgdb)
        db = client.local
        db.authenticate(mongodata.user, mongodata.passwd)
        col = db['Instagram']
    else:
        col = None
    timeout = cityparams[city][4]

    wsinf = (args.webservice == 1)


    ## Gets instagram Data at interval times
    while True:
        get_instagram(city, logger, col, wsinf=wsinf)
        sleep(timeout)
        if args.mongo == 1 and not client.alive():
            col = None