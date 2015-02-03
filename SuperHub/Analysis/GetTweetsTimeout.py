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

from src.Twitter.TwitterGetterTimeout import get_tweets, config_logger


# City parameter
city = 'paris'

logger = config_logger(silent=True)
while True:
    get_tweets(city, logger)
    sleep(10)
