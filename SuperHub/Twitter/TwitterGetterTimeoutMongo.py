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

import time
import logging
import signal
import socket

from TwitterAPI import TwitterAPI
from requests import RequestException
from requests.exceptions import Timeout

from requests.packages.urllib3.exceptions import ReadTimeoutError
from pymongo import MongoClient
import requests
from pymongo.errors import DuplicateKeyError

from Parameters.Constants import cityparams, TW_TIMEOUT, homepath
from Parameters.Private import credentials, Webservice
from Parameters.Pconstants import mglocal


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


def get_tweets(city, logger, col, inform=50, wsinf=True):
    """
    GEt tweets waiting ot a timeout

    @param city:
    @param logger:
    @param silent:
    @return:
    """

    initime = int(time.time())
    if col is None:
        wfile = open(homepath + cityparams[city][2] + '-twitter-py-%d.csv' % initime, 'w')
    else:
        wfile = None

    # Set the handler for the SIGALRM signal:
    signal.signal(signal.SIGALRM, _timeout)
    # Send the SIGALRM signal in TW_TIMEOUT seconds:
    signal.alarm(TW_TIMEOUT)
    minLat = cityparams[city][1][0]
    maxLat = cityparams[city][1][1]
    minLon = cityparams[city][1][2]
    maxLon = cityparams[city][1][3]

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
                    if col is not None:
                        tomongo = transform(vals, city)
                        try:
                            col.insert(tomongo)
                            logger.info('TWID: %s', tomongo['twid'])
                        except DuplicateKeyError:
                            logger.info('Duplicate: %s',  tomongo['twid'])
                    else:
                        if wfile is None:
                            wfile = open(homepath + cityparams[city][2] + '-twitter-py-%d.csv' % initime, 'w')
                        cnt = 0
                        for v in vals:
                            if type(v) is float:
                                wfile.write(str(v))
                            elif type(v) is unicode:
                                wfile.write(v.encode('utf8', 'replace').rstrip())
                            else:
                                wfile.write(v)
                            cnt += 1
                            if cnt < len(vals):
                                wfile.write('; ')

                        wfile.write('\n')
                        wfile.flush()

                # else:
                #     print 'Outside Bounding Box'
                #     print minLat, vals[2], maxLat
                #     print minLon, vals[1], maxLon

                currtime = int(time.time())
                deltatime = (currtime - initime) / 60.0
                if deltatime != 0:
                    logger.info('---- %2.3f tweets/minute', i/deltatime)

                i += 1
                if wsinf and inform != 0 and i%inform == 0:
                    try:
                        requests.get(Webservice, params={'content': city+'-twt', 'count': i, 'delta': i/deltatime})
                    except Timeout:
                        wsinf = False

            j += 1

    except TimeoutException:
        logger.info('##########################  It timed out! ###############################')
    except ReadTimeoutError:
        logger.info('##########################  It timed out! ###############################')
    except RequestException:
        logger.info('##########################  ERROR ###############################')
        wsinf = False


    if col is None:
        wfile.close()
