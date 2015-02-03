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


# City parameter
city = 'rome'

logger = config_logger(silent=True)
while True:
    get_tweets(city, logger)
    sleep(10)
