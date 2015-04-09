"""
.. module:: GetData

GetData
*************

:Description: GetData

    

:Authors: bejar
    

:Version: 

:Created on: 24/02/2014 14:08 

"""

__author__ = 'bejar'

from Parameters.Constants import bcnparam
from Analysis import DB


# DB.getApplicationData(milanparam, 'twitter')
# DB.getApplicationData(milanparam, 'instagram')

DB.getApplicationDataInterval(bcnparam, 'twitter', 1412114400)
DB.getApplicationDataInterval(bcnparam, 'instagram', 1412114400)
# DB.getApplicationDataInterval(hlsnkparam, 'twitter', 1409729400)
# DB.getApplicationDataInterval(hlsnkparam, 'instagram', 1408659300)
# DB.getApplicationDataInterval(hlsnkparam, 'twitter', 1380578300, 1409800000)
#DB.getApplicationDataOne(hlsnkparam, 'twitter')
