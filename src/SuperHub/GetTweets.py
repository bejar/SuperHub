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
from Constants import homepath, bcnparam

CONSUMER_KEY = 'U9AT8T0I6hZzOShihJB9106LB'
CONSUMER_SECRET = 'dW2mxwf5UIU7XcZOqJAvYnDkzjyM4q8ZDo98XHEfCSBUuwRiwd'
ACCESS_TOKEN_KEY = '241178901-XjwcAiPaW6cP0U47hsqsYcKmXCG56skcRmfXXxdj'
ACCESS_TOKEN_SECRET = 'Gnd0QTqZ111yrGWRoZBvtTXFI4lzLb4Mp0VKsg1ZGUcmZ'


api = TwitterAPI(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN_KEY,
    ACCESS_TOKEN_SECRET)


city = bcnparam[2]
initime = int(time.time())

wfile = open(homepath + city + '-twitter%d.csv'%initime, 'w')
locstr= '%s,%s,%s,%s' % (str(bcnparam[1][2]), str(bcnparam[1][0]), str(bcnparam[1][3]), str(bcnparam[1][1]))

r = api.request('statuses/filter', {'locations': locstr})


i = 0
j = 0
for item in r:
    if item['geo'] is not None:
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
        vals.append(str(item['geo']['coordinates'][1]))
        vals.append(str(item['geo']['coordinates'][0]))
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