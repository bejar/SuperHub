"""
.. module:: SuperHubTest2

SuperHubTest2
*************

:Description: SuperHubTest2

    

:Authors: bejar
    

:Version: 

:Created on: 27/02/2014 12:14 

"""

__author__ = 'bejar'

import urllib

from Analysis.DB import getTweets


#rfile = open(homepath + 'twitter+fsq.csv', 'w')
#rfile.write('#lat; lng; time; user; geohash; url\n')


tw = getTweets(time=1383399900)

i = 0
for t in tw:
    if 'http' in t['text']:
        text = t['text'].split()
        url = None
        for p in text:
            if 'http' in p:
                url = p
        if url is not None:
            try:
                resp = urllib.urlopen(url)
                if 'instagram' in resp.url:
                    i += 1
                    print i, t['interval'],
                    print t['text']
                    print resp.url
#                    if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
#                        rfile.write(str(t['lat']) + '; ' + str(t['lng']) + '; '
#                                    + str(t['interval']) + ';' + str(t['user'])
#                                    + '; ' + t['geohash']
#                                    + '; ' + resp.url.rstrip() + '\n')
#                        rfile.flush()

            except IOError:
                pass
            except UnicodeError:
                pass

#rfile.close()

print i




