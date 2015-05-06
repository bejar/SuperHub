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
from requests.exceptions import Timeout
from requests import RequestException
import folium
from pymongo.errors import DuplicateKeyError
from simplejson.scanner import JSONDecodeError
from requests.exceptions import ConnectionError
import OpenSSL

from Parameters.Constants import homepath, cityparams
from Parameters.Private import ig_credentials
from Parameters.Private import Webservice


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
    mymap = folium.Map(location=[(minLat + maxLat) / 2.0, (minLon + maxLon) / 2.0], zoom_start=12, width=1200,
                       height=800)

    for i, j in coords:
        mymap.circle_marker(location=[i, j],
                            radius=10, popup=str(i) + ' ' + str(j),
                            line_color='#FF0000',
                            fill_color='#110000')

    for i, j in cent:
        mymap.circle_marker(location=[i, j],
                            radius=6000, popup=str(i) + ' ' + str(j),
                            line_color='#0000FF',
                            fill_color='#000011')

    mymap.create_map(path=homepath + 'Results/Maps/' + city[2] + '-' + nfile + '.html')


def config_logger(silent=False, file=None):
    if file is not None:
        logging.basicConfig(filename=homepath + '/' + file + '.log', filemode='w')
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


def get_instagram(city, logger, col, wsinf=True):
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
    if col is None:
        wfile = open(homepath + cityparams[city][2] + '-instagram-py-%d.csv' % itime, 'w')
    else:
        wfile = None

    iphotos = {}
    for circ in lcircles:
        try:
            api = requests.get(
                'https://api.instagram.com/v1/media/search?lat=%f&lng=%f&distance=5000&count=100&min_timestamp=%d&max_timestamp=%d&access_token=%s' %
                (circ[0], circ[1], itime - timeout, itime, access_token))
            res = api.json()

            for media in res['data']:
                mid = media['id']
                capt = ''

                try:
                    if media['user'] is not None:
                        iphotos[mid] = {'city': city,
                                        'igid': mid,
                                        'user': media['user']['id'],
                                        'lat': media['location']['latitude'],
                                        'lng': media['location']['longitude'],
                                        'time': media['created_time'],
                                        'text': capt
                                        }
                        if 'caption' in media:
                            v = media['caption']
                            if v is not None and 'text' in v:
                                iphotos[mid]['text'] = v['text'].strip()
                            else:
                                iphotos[mid]['text'] = ''
                        else:
                            iphotos[mid]['text'] = ''
                        if 'name' in media['location']:
                            iphotos[mid]['name'] = media['location']['name'].strip()
                        else:
                            iphotos[mid]['name'] = ''
                        if 'id' in media['location']:
                            iphotos[mid]['iglocid'] = str(media['location']['id'])

                except TypeError:
                    logger.error('TypeError')
                except KeyError:
                    logger.error('KeyError')
        except JSONDecodeError:
            logger.error('EMPTY')
        except ConnectionError:
            logger.error('Connection Error')
        except OpenSSL.SSL.SysCallError:
            logger.error('SSL Error')

    lcoord = [(iphotos[v]['lat'], iphotos[v]['lng']) for v in iphotos]
    logger.info('---- %d photos # %s', len(iphotos), time.ctime(time.time()))
    # MapThis(cityparams[city], lcoord, lcircles, city)

    i = 0
    for v in iphotos:
        if col is not None:
            try:
                col.insert(iphotos[v])
                i += 1
            except DuplicateKeyError:
                logger.info('Duplicate: %s', v)
        else:
            if wfile is None:
                wfile = open(homepath + cityparams[city][2] + '-instagram-py-%d.csv' % itime, 'w')

            cnt = 0
            for att in lattr:

                if att in iphotos[v]:
                    try:
                        if type(iphotos[v][att]) is float:
                            wfile.write(str(iphotos[v][att]))
                        elif type(iphotos[v][att]) is unicode:
                            #wfile.write(str(iphotos[v][att]).encode('utf8', 'replace').rstrip())
                            wfile.write(
                                iphotos[v][att].encode('utf8', 'replace').replace('\n', ' ').replace('\r', '').rstrip())
                        else:
                            wfile.write(iphotos[v][att])

                    except UnicodeEncodeError:
                        logger.error('Unicode Encode Error')
                        wfile.write('')
                else:
                    wfile.write('')
                cnt += 1
                if cnt < len(lattr):
                    wfile.write('; ')

            wfile.write('\n')
            wfile.flush()
    if wsinf:
        try:
            requests.get(Webservice, params={'content': city + '-ig', 'count': i, 'delta': i / (timeout / 60)})
        except Timeout:
            logger.error('Webservice Timeout')
            wsinf = False
        except RequestException:
            logger.error('Webservice Request Exception')
            wsinf = False


lattr = ['city', 'igid', 'user', 'lat', 'lng', 'time', 'text', 'name']