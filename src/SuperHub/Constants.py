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

mgdbbcn = 'mongodb://atalaya-barcelona.mooo.com:27017/'
mgdbmilan = 'mongodb://atalaya-milan.mooo.com:27017/'
mgdbhelsinki = 'mongodb://atalaya-helsinki.mooo.com:27017/'

msqldb = 'polaris.lsi.upc.edu'
msqluser = 'superhub'
msqlpass = 'superhub'
msqldbs = 'SuperHub'

# 45.467 9.200
bcncoord = (41.24, 41.52, 1.95, 2.34)
milancoord = (45.33, 45.59, 9.03, 9.37)
hlsnkcoord = (60.02, 60.30, 24.72, 25.10)
pariscoord = (48.37, 48.65, 2.01, 2.41)
londoncoord = (51.16, 51.45, -0.13, 0.27)
berlincoord = (52.16, 52.45, 13.03, 13.43)

homepath = '/home/bejar/Data/SuperHub/'
bcnparam = (mgdbbcn, bcncoord, 'bcn')
milanparam = (mgdbmilan, milancoord, 'milan')
hlsnkparam = (mgdbhelsinki, hlsnkcoord, 'hlsnk')
parisparam = (None, pariscoord, 'paris')
londonparam = (None, londoncoord, 'london')
berlinparam = (None, berlincoord, 'berlin')

cityparams ={
    'bcn': bcnparam,
    'milan': milanparam,
    'paris': parisparam,
    'london': londonparam,
    'berlin': berlinparam
}