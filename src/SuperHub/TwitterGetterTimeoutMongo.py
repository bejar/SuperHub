"""
.. module:: TwitterGetter

gettweets
*************

:Description:

 Function to get tweets from a city



:Authors: bejar


:Version:

:Created on: 01/12/2014 7:38

"""

__author__ = 'bejar'



from TwitterAPI import TwitterAPI
import time
from Constants import homepath, cityparams, TW_TIMEOUT
from Private import credentials
import logging
import signal
import requests
import socket
from requests import RequestException
from requests.packages.urllib3.exceptions import ReadTimeoutError
from pymongo import MongoClient
from Pconstants import mglocal

class TimeoutException(Exception):
    """ Simple Exception to be called on timeouts. """
    pass


def transform(tdata, city):
   return {'city': city,
        'twid': tdata[0],
        'lat': tdata[2],
        'lng': tdata[1],
        'time': str(tdata[3]),
        'user': tdata[4],
        'uname': tdata[5],
        'tweet': tdata[6]
      }



def _timeout(signum, frame):
    """ Raise an TimeoutException.

    This is intended for use as a signal handler.
    The signum and frame arguments passed to this are ignored.

    """
    # Raise TimeoutException with system default timeout message
    raise TimeoutException()


def config_logger(silent=False):

    mgdb = mglocal[0]
    client = MongoClient(mgdb)
    db = client.local
    db.authenticate(mglocal[2], password=mglocal[3])
    col = db[mglocal[1]]


    # Logging configuration
    logger = logging.getLogger('log')
    if silent:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)

    console = logging.StreamHandler()
    if silent:
        console.setLevel(logging.ERROR)
    else:
        console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('log').addHandler(console)
    return logger


def get_tweets(city, logger, inform=50):
    """
    GEt tweets waiting ot a timeout

    @param city:
    @param logger:
    @param silent:
    @return:
    """

    initime = int(time.time())
    hostname = socket.gethostname()
    address = "http://" + hostname + ":8890/Update"

    # Set the handler for the SIGALRM signal:
    signal.signal(signal.SIGALRM, _timeout)
    # Send the SIGALRM signal in TW_TIMEOUT seconds:
    signal.alarm(TW_TIMEOUT)
    minLat = cityparams[city][1][0]
    maxLat = cityparams[city][1][1]
    minLon = cityparams[city][1][2]
    maxLon =  cityparams[city][1][3]

    try:
        api = TwitterAPI(
            credentials[city][0],credentials[city][1],credentials[city][2],credentials[city][3])

        locstr = '%s,%s,%s,%s' % (str(cityparams[city][1][2]), str(cityparams[city][1][0]), str(cityparams[city][1][3]), str(cityparams[city][1][1]))

        r = api.request('statuses/filter', {'locations': locstr})

        i = 0
        j = 0
        for item in r.get_iterator():
            if 'limit' in item:
                logger.error('%d tweets missed', item['limit'].get('track'))
            elif 'disconnect' in item:
                logger.error('disconnecting because %s', item['disconnect'].get('reason'))
                return 0
            elif item['coordinates'] is not None:
                vals = []
                logger.info('TW: %d', i)
                if 'text' in item:
                    logger.info('Text: %s', item['text'].replace('\n', ' ').replace('\r', ''))
                logger.info('Time: %s', time.ctime(int(item['timestamp_ms'][0:-3])))
                logger.info('ID: %s', str(item['user']['id']))

                vals.append(str(item['id']))
                vals.append(float(item['coordinates']['coordinates'][0]))
                vals.append(float(item['coordinates']['coordinates'][1]))
                vals.append(str(int(item['timestamp_ms'][0:-3])))
                vals.append(str(item['user']['id']))
                vals.append(str(item['user']['screen_name']))


                if 'text' in item:
                    vals.append('(### %s ###)' % item['text'].replace('\n', ' ').replace('\r', ''))
                else:
                    vals.append('(## ##)')

                if (minLat <= vals[2] < maxLat) and (minLon <= vals[1] < maxLon):
                    print transform(vals, city)
                    # col.insert(transform(vals, city))
                else:
                    print 'Outside Bounding Box'
                    print minLat, vals[2], maxLat
                    print minLon, vals[1], maxLon

                currtime = int(time.time())
                deltatime = (currtime - initime) / 60.0
                logger.info('---- %2.3f tweets/minute', i/deltatime)


                i += 1
                # if inform != 0 and i%inform == 0:
                #     requests.get(address, params={'content': city})
            j += 1

    except TimeoutException:
        logger.info('##########################  It timed out! ###############################')
    except ReadTimeoutError:
        logger.info('##########################  It timed out! ###############################')
    except RequestException:
        logger.info('##########################  ERROR ###############################')


