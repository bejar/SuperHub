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
mguser = 'superhubadmin'
mgpass = '1988glmek'
msqldb = 'polaris.lsi.upc.edu'
msqluser = 'superhub'
msqlpass = 'superhub'
msqldbs = 'SuperHub'
# 45.467 9.200
bcncoord = (41.24, 41.52, 1.95, 2.34)
milancoord = (45.33, 45.59, 9.03, 9.37)
hlsnkcoord = (60.02, 60.30, 24.72, 25.10)
homepath = '/home/bejar/Data/SuperHub/'
bcnparam = (mgdbbcn, bcncoord, 'bcn')
milanparam = (mgdbmilan, milancoord, 'milan')
hlsnkparam = (mgdbhelsinki, hlsnkcoord, 'hlsnk')

# Twitter Credentials

CONSUMER_KEY = 'U9AT8T0I6hZzOShihJB9106LB'
CONSUMER_SECRET = 'dW2mxwf5UIU7XcZOqJAvYnDkzjyM4q8ZDo98XHEfCSBUuwRiwd'
ACCESS_TOKEN_KEY = '241178901-XjwcAiPaW6cP0U47hsqsYcKmXCG56skcRmfXXxdj'
ACCESS_TOKEN_SECRET = 'Gnd0QTqZ111yrGWRoZBvtTXFI4lzLb4Mp0VKsg1ZGUcmZ'
