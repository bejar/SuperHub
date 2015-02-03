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

import requests
import folium

from Parameters.Constants import homepath, cityparams
from Parameters.Private import ig_credentials


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



city = 'milan'
access_token = ig_credentials[city]['Token']
lcircles = cityparams[city][3]
itime = int(time.time())
iphotos = {}
for circ in lcircles:
    api = requests.get('https://api.instagram.com/v1/media/search?lat=%f&lng=%f&distance=5000&count=200&min_timestamp=%d&max_timestamp=%d&access_token=%s' %
                       (circ[0], circ[1], itime - 3600, itime, access_token))
    res = api.json()
    for media in res['data']:
        mid = media['id']
        capt = ''
        print media
        if 'caption' in media:
            v = media['caption']
            if v is not None and 'text' in v:
                capt = v['text']

        print media['location'].keys()
        iphotos[mid] = {'igid': mid,
                  'uid': media['user']['id'],
                  'lat': media['location']['latitude'],
                  'lon': media['location']['longitude'],
                  'time': media['created_time'],
                  'text': capt
        }
        if 'name' in media['location']:
            print media['location']['name']
        print time.ctime(float(media['created_time'])), media['created_time']

lcoord = [(iphotos[v]['lat'], iphotos[v]['lon']) for v in iphotos]
print len(iphotos)
MapThis(cityparams[city], lcoord, lcircles, city)

#i = 0
# api = requests.get('https://api.instagram.com/v1/media/search?lat=41.23&lng=2.09&min_timestamp=1422879173&distance=2000&access_token=%s' %access_token[0])
# res = api.json()
#
# for media in res['data']:
#   print media.keys()
#   print media['user']
#   print media['location']
#   i += 1
#
# print '------------------', i
