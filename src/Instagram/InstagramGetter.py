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

import requests
import time
import folium
from Constants import homepath, cityparams, IG_TIMEOUT
import logging
from pymongo.errors import DuplicateKeyError

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

def MapThis(city, coords, nfile):

    minLat, maxLat, minLon, maxLon = city[1]
    mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1200, height=800)

    for i, j in coords:
        mymap.circle_marker(location=[i, j],
                            radius=10, popup=str(i)+' '+str(j),
                            line_color='#FF0000',
                            fill_color='#110000')

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
    client_id = 'c1ea5533e5634fd58870220b4adc5851'
    client_secret = 'e7eb412c9990464db0aabfc33e4ba517'
    redirect_uri = 'http://polaris.lsi.upc.edu:9999/Instagram'

    access_token = (u'1684203437.c1ea553.2fa85716cdd14d5fbf2b98f94496c6d9',
                    {u'username': u'javier.bejar', u'bio': u'', u'website': u'', u'profile_picture': u'https://instagramimages-a.akamaihd.net/profiles/anonymousUser.jpg', u'full_name': u'Javier Bejar', u'id': u'1684203437'})

    lcircles = cityparams[city][3]
    itime = int(time.time())
    iphotos = {}
    for circ in lcircles:
        api = requests.get('https://api.instagram.com/v1/media/search?lat=%f&lng=%f&distance=5000&count=100&min_timestamp=%d&max_timestamp=%d&access_token=%s' %
                           (circ[0], circ[1], itime - 300, itime, access_token[0]))
        res = api.json()

        for media in res['data']:
            mid = media['id']
            capt = ''
            if 'caption' in media:
                v = media['caption']
                if v is not None and 'text' in v:
                    capt = v['text']

            iphotos[mid] = {'city': city,
                            'igid': mid,
                            'uid': media['user']['id'],
                            'lat': media['location']['latitude'],
                            'lon': media['location']['longitude'],
                            'time': media['created_time'],
                            'text': capt
            }

    lcoord = [(iphotos[v]['lat'], iphotos[v]['lon']) for v in iphotos]
    logger.info('---- %g photos', len(iphotos))
    MapThis(cityparams['bcn'], lcoord, 'bcn')

    for v in iphotos:
        try:
            col.insert(iphotos[v])
        except DuplicateKeyError:
            print 'Duplicate: ',  v
