"""
.. module:: InstagramGetter

InstagramGetter
*************

:Description: InstagramGetter

Getting photograph ingormation from instagram

:Authors: bejar
    

:Version: 

:Created on: 02/02/2015 8:27 

"""

__author__ = 'bejar'

import time
import logging

import requests
import folium
from pymongo.errors import DuplicateKeyError
from simplejson.scanner import JSONDecodeError

from Parameters.Constants import homepath, cityparams
from Parameters.Private import ig_credentials


class TimeoutException(Exception):
    """ Simple Exception to be called on timeouts. """
    pass

def _timeout(signum, frame):
    """ Raise an TimeoutException.

    This is intended for use as a signal handler.
    The signum and frame arguments passed to this are ignored.

    """
    # Raise TimeoutException with system default timeout message
    raise TimeoutException()

def MapThis(city, coords, cent, nfile):

    minLat, maxLat, minLon, maxLon = city[1]
    mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1200, height=800)

    for i, j in coords:
        mymap.circle_marker(location=[i, j],
                            radius=10, popup=str(i)+' '+str(j),
                            line_color='#FF0000',
                            fill_color='#110000')

    for i, j in cent:
        mymap.circle_marker(location=[i, j],
                            radius=6000, popup=str(i)+' '+str(j),
                            line_color='#0000FF',
                            fill_color='#000011')

    mymap.create_map(path=homepath + 'Results/Maps/' + city[2] + '-' + nfile + '.html')

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


def get_instagram(city, logger, col):
    """
    Gets Instagram data from a city and inserts in a Mongo DB

    @param city:
    @param logger:
    @param col:
    @return:
    """
    access_token = ig_credentials[city]['Token']
    lcircles = cityparams[city][3]
    timeout = cityparams[city][4]

    itime = int(time.time())
    iphotos = {}
    for circ in lcircles:
        api = requests.get('https://api.instagram.com/v1/media/search?lat=%f&lng=%f&distance=5000&count=100&min_timestamp=%d&max_timestamp=%d&access_token=%s' %
                           (circ[0], circ[1], itime - timeout, itime, access_token))
        try:
            res = api.json()

            for media in res['data']:
                mid = media['id']
                capt = ''

                iphotos[mid] = {'city': city,
                                'igid': mid,
                                'uid': media['user']['id'],
                                'lat': media['location']['latitude'],
                                'lon': media['location']['longitude'],
                                'time': media['created_time'],
                                'text': capt
                }
                if 'caption' in media:
                    v = media['caption']
                    if v is not None and 'text' in v:
                         iphotos[mid]['text']= v['text']
                if 'name' in media['location']:
                    iphotos[mid]['name'] = media['location']['name']
        except JSONDecodeError:
            logger.info('EMPTY')

    lcoord = [(iphotos[v]['lat'], iphotos[v]['lon']) for v in iphotos]
    logger.info('---- %d photos # %s', len(iphotos), time.ctime(time.time()))
    MapThis(cityparams[city], lcoord, lcircles, city)

    for v in iphotos:
        try:
            col.insert(iphotos[v])
        except DuplicateKeyError:
            logger.info('Duplicate: %s',  v)
