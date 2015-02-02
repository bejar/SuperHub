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


# access_token = "YOUR_ACCESS_TOKEN"
# api = InstagramAPI(access_token=access_token)
# recent_media, next_ = api.user_recent_media(user_id="userid", count=10)
# for media in recent_media:
#    print media.caption.text


api = InstagramAPI(client_id=ig_credentials['ID'], client_secret=ig_credentials['Secret'])
popular_media = api.media_popular(count=20)
for media in popular_media:
    print media.images['standard_resolution'].url