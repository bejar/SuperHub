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
from Constants import homepath, cityparams
from Private import credentials
import logging


def get_tweets(city):

    # Logging configuration
    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('log').addHandler(console)

    api = TwitterAPI(
        credentials[city][0],credentials[city][1],credentials[city][2],credentials[city][3])

    initime = int(time.time())

    wfile = open(homepath + cityparams[city][2] + '-twitter-py-%d.csv'%initime, 'w')
    locstr = '%s,%s,%s,%s' % (str(cityparams[city][1][2]), str(cityparams[city][1][0]), str(cityparams[city][1][3]), str(cityparams[city][1][1]))

    r = api.request('statuses/filter', {'locations': locstr})

    i = 0
    j = 0
    for item in r:
        if 'limit' in item:
            logger.info('%d tweets missed', item['limit'].get('track'))
        elif 'disconnect' in item:
            logger.info('disconnecting because %s', item['disconnect'].get('reason'))
            wfile.close()
            return 0
        elif item['coordinates'] is not None:
            vals = []
            logger.info('TW: %d', i)
            if 'text' in item:
                logger.info('Text: %s', item['text'])
            logger.info('Time: %s', time.ctime(int(item['timestamp_ms'][0:-3])))
            logger.info('ID: %s', str(item['user']['id']))

            vals.append(str(item['id']))
            vals.append(str(item['user']['screen_name']))
            vals.append(str(item['user']['id']))
            vals.append(str(item['coordinates']['coordinates'][0]))
            vals.append(str(item['coordinates']['coordinates'][1]))
            vals.append(str(int(item['timestamp_ms'][0:-3])))
            if 'text' in item:
                vals.append('(### %s ###)'%item['text'])
            else:
                vals.append('(####)')

            cnt = 0
            for v in vals:
                wfile.write(v.encode('ascii', 'ignore').rstrip())
                cnt += 1
                if cnt < len(vals):
                    wfile.write('; ')

            wfile.write('\n')
            wfile.flush()

            currtime = int(time.time())
            deltatime = (currtime - initime) / 60.0
            logger.info('---- %2.3f tweets/minute', i/deltatime)


            i += 1
        j += 1

