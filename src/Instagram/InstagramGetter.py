"""
.. module:: InstagramGetter

InstagramGetter
*************

:Description: InstagramGetter

    

:Authors: bejar
    

:Version: 

:Created on: 02/02/2015 8:27 

"""

__author__ = 'bejar'

from Private import ig_credentials
from instagram.client import InstagramAPI

client_id = 'c1ea5533e5634fd58870220b4adc5851'
client_secret = 'e7eb412c9990464db0aabfc33e4ba517'
redirect_uri = 'http://polaris.lsi.upc.edu:9999/Instagram'


api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope='')

access_token = api.exchange_code_for_access_token("8a88fe0ad33b4886b4f7ba398ded3677")
print access_token
#access_token = "acccb47475b540ef93096bd3cf12fdfc"
api = InstagramAPI(access_token=access_token)
recent_media, next_ = api.user_recent_media(user_id="javier.bejar", count=10)
for media in recent_media:
   print media.caption.text


# api = InstagramAPI(client_id=ig_credentials['ID'], client_secret=ig_credentials['Secret'])
# popular_media = api.media_popular(count=20)
# for media in popular_media:
#    print media.images['standard_resolution'].url
