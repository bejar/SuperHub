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


from Twitter.TwitterGetter import get_tweets

# City parameter

city = 'rome'


while True:
    get_tweets(city)

