"""
.. module:: testcsv

testcsv
*************

:Description: testcsv

    

:Authors: bejar
    

:Version: 

:Created on: 02/04/2014 8:56 

"""

__author__ = 'bejar'

from Parameters.Constants import homepath

cdate = '20150223'
for city in ['bcn', 'milan', 'paris', 'rome', 'london', 'berlin']:

    fname = homepath + 'Data-py/instagram/' + city + '-instagram-' + cdate + '.data'
    rfile = open(fname, 'r')
    # wname = homepath + 'Data-py/foursquare/' + city + '-fsq-f-twitter-'+ cdate + '.data.corr'
    # wfile = open(wname, 'w')
    print '----------------', city

    cnt = 0
    for lines in rfile:
        vals = lines.split(';')
        if len(vals) != 9:
            print cnt, len(vals)
            # wfile.write(lines)
            # else:
            cnt += 1
    print cnt

