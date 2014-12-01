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

from TwitterAPI import TwitterAPI
import time
from Constants import homepath, bcnparam, milanparam, hlsnkparam, parisparam
from Private import CONSUMER_KEY_BCN, CONSUMER_SECRET_BCN, ACCESS_TOKEN_KEY_BCN, ACCESS_TOKEN_SECRET_BCN
from Private import CONSUMER_KEY_PARIS, CONSUMER_SECRET_PARIS, ACCESS_TOKEN_KEY_PARIS, ACCESS_TOKEN_SECRET_PARIS


CONSUMER_KEY = CONSUMER_KEY_PARIS
CONSUMER_SECRET = CONSUMER_SECRET_PARIS
ACCESS_TOKEN_KEY = ACCESS_TOKEN_KEY_PARIS
ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET_PARIS


api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)

cityparam = parisparam

city = cityparam[2]
initime = int(time.time())

wfile = open(homepath + city + '-twitter-py-%d.csv'%initime, 'w')
locstr = '%s,%s,%s,%s' % (str(cityparam[1][2]), str(cityparam[1][0]), str(cityparam[1][3]), str(cityparam[1][1]))

print locstr

r = api.request('statuses/filter', {'locations': locstr})
print 'Begins'

i = 0
j = 0
for item in r:
    if 'limit' in item:
        print '%d tweets missed' % item['limit'].get('track')
    elif 'disconnect' in item:
        print 'disconnecting because %s' % item['disconnect'].get('reason')
        break
    elif item['coordinates'] is not None:
        vals = []
        print
        print 'TW:', i
        print 'Text:', item['text'] if 'text' in item else ' '
        print 'Time:', time.ctime(int(item['timestamp_ms'][0:-3]))
        print 'ID:', item['user']['id']
        print '-----'


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

        cnt= 0
        for v in vals:
            wfile.write(v.encode('ascii', 'ignore').rstrip())
            cnt += 1
            if cnt < len(vals):
                wfile.write('; ')

        wfile.write('\n')
        wfile.flush()


        i += 1
    j += 1
    print j,