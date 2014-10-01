"""
.. module:: DrawMap

DrawMap
*************

:Description: DrawMap

   Functions for drawing routes in a map

:Authors: bejar
    

:Version: 

:Created on: 01/10/2014 10:06 

"""

__author__ = 'bejar'

from Constants import homepath
import folium
from geojson import LineString, GeometryCollection, FeatureCollection, Feature
import geojson


def MapThis(city, routes, nfile):

    minLat, maxLat, minLon, maxLon = city[1]
    mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1200, height=800)
    lcoord = []
    for coord in routes:
        c = coord.split('#')
        lcoord.append((float(c[0]), float(c[1])))

    lgeo = []

    for i in range(len(lcoord)-1):
        x1 = lcoord[i][0]
        y1 = lcoord[i][1]
        x2 = lcoord[i+1][0]
        y2 = lcoord[i+1][1]

        lgeo.append(Feature(geometry=LineString([(y1,x1), (y2, x2)])))

    geoc = FeatureCollection(lgeo)
    dump = geojson.dumps(geoc)
    jsfile = open(homepath + 'Results/Maps/' + city[2] +'-' + nfile + '.json', 'w')
    jsfile.write(dump)
    jsfile.close()
    mymap.geo_json(geo_path=homepath + 'Results/Maps/'+ city[2] +'-' + nfile + '.json', fill_color='Black', line_color='Black', line_weight=3)
    mymap.create_map(path=homepath + 'Results/Maps/' +  city[2] +'-' + nfile + '.html')

