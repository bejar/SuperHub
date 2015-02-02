# -*- coding: utf-8 -*-
"""
.. module:: SuperHubConstants

Constants
************

:Description: SuperHub constants,

    The coordinates of the region of interest and the path to the data files
    And the information of the mongo database

:Authors:
    bejar

:Version: 1.0


"""

__author__ = 'bejar'

from Pconstants import mgdbbcn, mgdbmilan, mgdbhelsinki

homepath = '/home/bejar/Data/SuperHub/'

# 45.467 9.200
bcncoord = (41.24, 41.59, 1.95, 2.34)
milancoord = (45.33, 45.59, 9.03, 9.37)
hlsnkcoord = (60.02, 60.30, 24.72, 25.10)
pariscoord = (48.52, 49.05, 1.97, 2.68)
londoncoord = (51.23, 51.8, -0.50, 0.37)
berlincoord = (52.32, 52.62, 13.11, 13.60)
romecoord = (41.78, 42.0, 12.33, 12.62)
bcnigcircles = [(41.37, 2.15), (41.42,2.20), (41.31, 2.10), (41.45, 2.07)]

bcnparam = (mgdbbcn, bcncoord, 'bcn', bcnigcircles)
milanparam = (mgdbmilan, milancoord, 'milan')
hlsnkparam = (mgdbhelsinki, hlsnkcoord, 'hlsnk')
parisparam = (None, pariscoord, 'paris')
londonparam = (None, londoncoord, 'london')
berlinparam = (None, berlincoord, 'berlin')
romeparam = (None, romecoord, 'rome')

cityparams ={
    'bcn': bcnparam,
    'milan': milanparam,
    'paris': parisparam,
    'london': londonparam,
    'berlin': berlinparam,
    'rome': romeparam
}

TW_TIMEOUT = 3600 # 1 hour
IG_TIMEOUT = 300 # 5 minutes