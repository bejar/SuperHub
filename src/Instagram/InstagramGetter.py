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


client_id = 'c1ea5533e5634fd58870220b4adc5851'
client_secret = 'e7eb412c9990464db0aabfc33e4ba517'
redirect_uri = 'http://polaris.lsi.upc.edu:9999/Instagram'
scope = ''

access_token = (u'1684203437.c1ea553.2fa85716cdd14d5fbf2b98f94496c6d9',
                {u'username': u'javier.bejar', u'bio': u'', u'website': u'', u'profile_picture': u'https://instagramimages-a.akamaihd.net/profiles/anonymousUser.jpg', u'full_name': u'Javier Bejar', u'id': u'1684203437'})

api = requests.get('https://api.instagram.com/v1/media/search?lat=48.858844&lng=2.294351&distance=3000&count=100&min_timestamp=1422879173&max_timestamp=1422879303&access_token=%s' %access_token[0])
res = api.json()
i = 0
print res['data'][0].keys()
for media in res['data']:
  print media['user']['id']
  print media['location']
  print media['type']
  print media['id']
  if 'caption' in media:
      v = media['caption']
      if v is not None and 'text' in v:
            print v['text']
      else:
          print '******************************************'
  print time.ctime(float(media['created_time']))
  i += 1

print '------------------', i

i = 0
# api = requests.get('https://api.instagram.com/v1/media/search?lat=41.32&lng=1.21&distance=2000&access_token=%s' %access_token[0])
# res = api.json()
#
# for media in res['data']:
#   print media.keys()
#   print media['user']
#   print media['location']
#   i += 1
#
# print '------------------', i
