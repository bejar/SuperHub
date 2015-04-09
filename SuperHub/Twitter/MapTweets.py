"""
.. module:: MapTweets

MapTweets
*************

:Description: MapTweets

    

:Authors: bejar
    

:Version: 

:Created on: 02/12/2014 10:58 

"""

__author__ = 'bejar'

import time

import folium

from Parameters.Constants import homepath, cityparams


def map_all(city):
    rfile = open(homepath + 'Data-py/' + city + '-py.data', 'r')
    minLat, maxLat, minLon, maxLon = cityparams[city][1]
    mymap = folium.Map(location=[(minLat + maxLat) / 2.0, (minLon + maxLon) / 2.0], zoom_start=12, width=1200,
                       height=1200)

    for lines in rfile:
        vals = lines.split(';')
        long = vals[3]
        lat = vals[4]
        mymap.circle_marker(location=[lat, long],
                            radius=10,
                            line_color='#FF0000',
                            fill_color='#110000')
    mymap.create_map(path=homepath + 'Data-py/' + city + '-py' + '.html')


def map_hours(city, h_init, h_end):
    rfile = open(homepath + 'Data-py/' + city + '-py.data', 'r')
    minLat, maxLat, minLon, maxLon = cityparams[city][1]
    mymap = folium.Map(location=[(minLat + maxLat) / 2.0, (minLon + maxLon) / 2.0], zoom_start=12, width=1200,
                       height=1200)

    for lines in rfile:
        vals = lines.split(';')
        etime = time.gmtime(int(vals[5]))
        if h_init <= etime.tm_hour < h_end:
            long = vals[3]
            lat = vals[4]
            mymap.circle_marker(location=[lat, long],
                                radius=10,
                                line_color='#FF0000',
                                fill_color='#110000')  # ,popup=str(lat)+' '+str(long)
    mymap.create_map(path=homepath + 'Data-py/' + city + '-H' + str(h_init) + '-' + str(h_end) + '-py' + '.html')


for city in ['bcn', 'london', 'paris', 'rome', 'milan', 'berlin']:
    map_hours(city, 22, 24)

