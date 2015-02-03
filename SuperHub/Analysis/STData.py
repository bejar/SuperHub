# -*- coding: utf-8 -*-
"""
.. module:: Data
.. moduleauthor:: Javier Béjar

STData
************

:Description: SuperHub STData class

    Representation for Spatio Temporal data, basically latitude, longitude and time events with the user that
    generated the event

    Performs different processings to the data matrix

:Authors:
    bejar

:Version: 1.0

:File: Data

:Created on: 18/02/2014 10:09

"""

__author__ = 'bejar'

import operator
import time

from numpy import loadtxt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from Parameters.Constants import homepath




#import pygmaps
import folium
from geojson import FeatureCollection, Feature, Polygon
import geojson
from Parameters.Pconstants import mglocal
from pymongo import MongoClient

pltcolors = ['#F00000', '#00F000', '#0000F0', '#0F0000', '#000F00', '#00000F']

class STData:
    """
    Class for a superhub dataset:

    :arg path: Sets the path of the file
    :arg application: Sets the application of the dataset

    """
    dataset = None
    application = None
    wpath = None
    mxhh = None
    mnhh = None
    lhh = None
    datasethh = None
    city = None

    def __init__(self, path, city, application):
        """
        Just sets the path and application for the dataset


         :arg path: Sets the path of the file
         :arg application: Sets the application of the dataset

        """
        self.application = application
        self.wpath = path
        self.city = city


    def read_DB(self):
        """
        Loads the data from a mongo DB

        """
        mgdb = mglocal[0]
        client = MongoClient(mgdb)
        db = client.local
        db.authenticate(mglocal[2], password=mglocal[3])
        col = db[mglocal[1]]
        minLat, maxLat, minLon, maxLon = self.city[1]
        cityname = self.city[2]

        c = col.find({'city': cityname,
                     'lat': {'$gt': minLat, '$lt': maxLat},
                     'lng': {'$gt': minLon, '$lt': maxLon},
                          #'time': {'$gt': intinit, '$lt': intend}
                    }, {'lat': 1, 'lng': 1, 'time': 1, 'user': 1}, timeout=False)

        qsize = c.count()
        self.dataset =  np.zeros((qsize,), dtype=('f8,f8,i32,S20'))
        cnt = 0
        for val in c:
            self.dataset[cnt][0] = val['lat']
            self.dataset[cnt][1] = val['lng']
            self.dataset[cnt][2] = val['time']
            self.dataset[cnt][3] = val['user']
            cnt += 1

    def read_data(self):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        fname = self.wpath + 'Data/' + self.city[2] + '-' + self.application + '.csv.bz2'
        self.dataset = loadtxt(fname, skiprows=1,
                               dtype=[('lat', 'f8'), ('lng', 'f8'), ('time', 'i32'), ('user', 'S20')],
                               usecols=(0, 1, 2, 3), delimiter=';', comments='#')

    def read_py_data(self):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        fname = self.wpath + 'Data-py/Data/' + self.city[2] + '-py.data.bz2'
        self.dataset = loadtxt(fname, skiprows=0,
                               dtype=[('lat', 'f8'), ('lng', 'f8'),  ('time', 'i32'), ('user', 'S20')],
                               usecols=(4, 3, 5, 2), delimiter=';', comments='*')


    def read_py_data_full(self, date=None):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        if date is None:
            fname = self.wpath + 'Data-py/Data/' + self.city[2] + '-py.data.bz2'
        else:
            fname = self.wpath + 'Data-py/Data/' + self.city[2] + '-py-'+ date + '.data'
        self.dataset = loadtxt(fname, skiprows=0,
                               dtype=[('twid', 'S25'), ('lat', 'f8'), ('lng', 'f8'),  ('time', 'i32'), ('user', 'S20'), ('uname', 'S20'), ('tweet', 'S250')],
                               usecols=(0, 4, 3, 5, 2, 1, 6), delimiter=';', comments='*')


    def read_py_instagram_data_full(self, date = None):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        if date is None:
            fname = self.wpath + 'Data-py/instagram/' + self.city[2] + '-instg-f-twitter.data.bz2'
        else:
            fname = self.wpath + 'Data-py/instagram/' + self.city[2] + '-instg-f-twitter-'+ date + '.data'
        self.dataset = loadtxt(fname, skiprows=0,
                               dtype=[('twid', 'S25'), ('lat', 'f8'), ('lng', 'f8'), ('igurl', 'S100'), ('igid', 'S20'), ('iguname', 'S20')],
                               usecols=(0, 1, 2, 5, 6, 7), delimiter=';', comments='*')

    def read_py_foursquare_data_full(self, date = None):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        if date is None:
            fname = self.wpath + 'Data-py/foursquare/' + self.city[2] + '-fsq-f-twitter.data.bz2'
        else:
            fname = self.wpath + 'Data-py/foursquare/' + self.city[2] + '-fsq-f-twitter-'+ date + '.data'
        self.dataset = loadtxt(fname, skiprows=0,
                               dtype=[('twid', 'S25'),
                                      ('fqurl', 'S50'),
                                      ('fqtime', 'S20'),
                                      ('fqid', 'S20'),
                                      ('gender', 'S8'),
                                      ('venueid', 'S20'),
                                      ('venuename', 'S50'),
                                      ('venuelat', 'S10'),
                                      ('venuelng', 'S10'),
                                      ('venuecat', 'S50'),
                                      ('venuepluralname', 'S20'),
                                      ('venueshortname', 'S20'),
                                      ('venueurl', 'S100')],
                               usecols=(0, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), delimiter=';', comments='*')


    def read_py_foursquare_data_full2(self, date = None):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        if date is None:
            fname = self.wpath + 'Data-py/foursquare/' + self.city[2] + '-fsq-f-twitter.data.bz2'
        else:
            fname = self.wpath + 'Data-py/foursquare/' + self.city[2] + '-fsq-f-twitter-'+ date + '.data'
        self.dataset = loadtxt(fname, skiprows=0, dtype=[('twid', 'S25'),
                                      ('fqurl', 'S50'),
                                      ('fqtime', 'S20'),
                                      ('fqid', 'S20'),
                                      ('gender', 'S8'),
                                      ('venueid', 'S20'),
                                      ('venuename', 'S50'),
                                      ('venuelat', 'S10'),
                                      ('venuelng', 'S10'),
                                      ('venuecat', 'S50'),
                                      ('venuepluralname', 'S20'),
                                      ('venueshortname', 'S20'),
                                      ('venueurl', 'S100')], delimiter=';', comments='*')



    def info(self):
        """
        Dumps some info about the dataset

        @return:
        """
        print 'A= ', self.application
        print 'C= ', self.city
        print 'D= ', self.dataset.shape

    def getDataCoordinates(self):
        """
        Returns an array with the coordinates of all the examples
        @return:
        """
        coord = np.zeros((self.dataset.shape[0], 2))
        for i in range(len(self.dataset)):
            coord[i, 0] = self.dataset[i][0]
            coord[i, 1] = self.dataset[i][1]
        return coord

    def compute_heavy_hitters(self, mxhh, mnhh, out=False):
        """
        Computes the list of the number of events
        and returns a list with the users between the
        positions mxhh and mnhh in the descendent order

        If the list heavy hitters have already been computed it is reused

        :param int mxhh: initial position of the heavy hitters list
        :param int mnhh: final position of the heavy hitters list

        :returns: list with the list of users ordered (desc) by number of events
        :rtype: list
        """
        print 'Computing Heavy Hitters ...'
        if self.lhh is not None:
            mnhht = min(mnhh, len(self.lhh))
            hhitters = [x for x, y in self.lhh[mxhh:mnhht]]
        else:
            usercount = {}
            for i in range(self.dataset.shape[0]):
                if self.dataset[i][3] in usercount:
                    usercount[self.dataset[i][3]] += 1
                else:
                    usercount[self.dataset[i][3]] = 1
            # we memorize the list of users so it can be reused
            sorted_x = sorted(usercount.iteritems(), key=operator.itemgetter(1), reverse=True)
            self.lhh = sorted_x
            mnhht = min(mnhh, len(sorted_x))
            hhitters = [x for x, y in sorted_x[mxhh:mnhht]]
            #print usercount[hhitters[0]], usercount[hhitters[-1]]
        return hhitters

    def select_heavy_hitters(self, mxhh, mnhh):
        """
        Deletes all the events that are not from the heavy hitters
        Returns a new data object only with the heavy hitters


        :param int mxhh: initial position of the heavy hitters list
        :param int mnhh: final position of the heavy hitters list

        :retuns:
         A list of the most active users in the indicated range
        """
        self.mxhh = mxhh
        self.mnhh = mnhh
        lhh = self.compute_heavy_hitters(mxhh, mnhh)
        print 'Selecting Heavy Hitters ...'
        return self.select_data_users(lhh)

    def select_data_users(self, users):
        """
        Selects only the events from the list of users

        :arg list users: List of users to select
        :returns:  Returns a new object with the selected users
        """
        print 'Selecting Users ...'
        # First transforms the list of users to a set to be efficient
        susers = set(users)
        # computes the boolean array for the selection
        sel = [self.dataset[i][3] in susers for i in range(self.dataset.shape[0])]
        asel = np.array(sel)
        data = STData(self.wpath, self.city, self.application)
        data.dataset = self.dataset[asel]
        data.mxhh = self.mxhh
        data.mnhh = self.mnhh
        return data

    # def select_hours(self, ihour, fhour):
    #     """
    #     Selects only events inside an specific range of hours
    #
    #     @param ihour:
    #     @param fhour:
    #     @return:
    #     """
    #     sel = []
    #     for i in range(self.dataset.shape[0]):
    #         stime = time.localtime(np.int32(self.dataset[i][2]))
    #         hour = stime[3]
    #         if ihour <= hour < fhour:
    #             sel.append(i)
    #     data = STData(self.wpath, self.city, self.application)
    #     data.dataset = self.dataset[sel]
    #     return data

    def select_hours(self, lhours):
        """
        Selects only events inside an specific range of hours

        @param ihour:
        @param fhour:
        @return:
        """
        sel = []
        for i in range(self.dataset.shape[0]):
            stime = time.localtime(np.int32(self.dataset[i][2]))
            hour = stime[3]
            for ih in lhours:
                ihour, fhour = ih
                if ihour <= hour < fhour:
                    sel.append(i)
        data = STData(self.wpath, self.city, self.application)
        data.dataset = self.dataset[sel]
        return data


    def hourly_table(self):
        """
        Computes the accumulated events by hour for the data table

        :returns:
         A list with the accumulated number of events for each hour of the day
        """
        htable = [0 for i in range(24)]
        for i in range(self.dataset.shape[0]):
            stime = time.localtime(np.int32(self.dataset[i][2]))
            evtime = stime[3]
            htable[evtime] += 1
        return htable

    def daily_table(self):
        """
        Computes the accumulated events by day for the data table

        :returns:
         A list with the accumulated number of events for each day of the week
        """
        htable = [0 for i in range(7)]
        for i in range(self.dataset.shape[0]):
            stime = time.localtime(np.int32(self.dataset[i][2]))
            evtime = stime[6]
            htable[evtime] += 1
        return htable

    def monthly_table(self):
        """
        Computes the accumulated events by month

        :returns:
         A list with the accumulated number of events for each mont of the year
        """
        htable = [0 for i in range(12)]
        for i in range(self.dataset.shape[0]):
            stime = time.localtime(np.int32(self.dataset[i][2]))
            evtime = stime[1]
            htable[evtime - 1] += 1
        return htable

    def contingency(self, scale, distrib=True, dataname=''):
        """
        Generates an scale x scale accumulated plot of the events

        :param int scale: Scale of the spatial discretization
        :param bool distrib: If returns the frequency or the accumulated events
        :param string dataname: Name to append to the filename
        """
        print 'Generating the plot ...'

        cont = np.zeros((scale, scale))
        minLat, maxLat, minLon, maxLon = self.city[1]
        normLat = scale / (maxLat - minLat)
        normLon = scale / (maxLon - minLon)

        # syn = (index, rel index, class)
        for i in range(self.dataset.shape[0]):
            posy = int(((self.dataset[i][0] - minLat) * normLat))
            posx = int(((self.dataset[i][1] - minLon) * normLon))
    #        print posx,posy,data[i][0],data[i][1], normLat, normLon
            try:
                if distrib:
                    cont[scale - posy - 1, posx - 1] += 1
                else:
                    cont[scale - posy - 1, posx - 1] = 1
            except IndexError:
                print self.dataset[i][0], self.dataset[i][1]
        if distrib:
            cont = cont / np.max(cont)

        fig = plt.figure()

        ax = fig.add_subplot(111)
        plt.title('Density ')

        plt.imshow(cont, interpolation='bicubic', cmap=cm.gist_yarg)
        vmax = np.max(cont)
        #    vmin=np.min(cont)

        if distrib:
            plt.colorbar(ticks=np.round(np.linspace(0, 1, 10), 2),
                         orientation='vertical')
        nfile = self.application + '-' + dataname

        fig.savefig(homepath + 'Results/' + self.city[2] + '-'+ nfile + '.pdf', orientation='landscape',format='pdf')

        #plt.show()

    def plot_events_grid(self, scale, distrib=True, dataname='', timeres=0):
        """
        Generates an scale x scale plot of the events
        Every event is represented by a point in the graph
        the ouput is a pdf file and an html file that uses open street maps

        :param int scale: Scale of the spatial discretization
        :param bool distrib: If returns the frequency or the accumulated events
        :param string dataname: Name to append to the filename
        """
        def plot_notimeres():
            """
            All time colapsed
            @return:
            """
            cont = np.zeros((scale, scale))
            for i in range(self.dataset.shape[0]):
                posy = int(((self.dataset[i][0] - minLat) * normLat))
                posx = int(((self.dataset[i][1] - minLon) * normLon))
                if distrib:
                    cont[scale - posy - 1, posx - 1] += 1
                else:
                    cont[scale - posy - 1, posx - 1] = 1

            if distrib:
                cont = cont / np.max(cont)
                plt.imshow(cont, interpolation='bicubic', cmap=cm.gist_yarg)
                for i in range(cont.shape[0]):
                    for j in range(cont.shape[1]):
                        if cont[i, j] > 0.01:
                            mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                radius=cont[i,j]*(circlesize/scale),
                                                line_color='#000000',
                                                fill_color='#110000')
                            # mymap.addradpoint(minLat+(((scale - i)+0.5)/normLat), minLon+((j+0.5)/normLon),
                            #                   cont[i,j]*(circlesize/scale), "#FF0000")
            else:
                for i in range(cont.shape[0]):
                    for j in range(cont.shape[1]):
                        if cont[i, j] > 0.01:
                            plt.plot(j, scale - i, 'k.')
                            mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                radius=30,
                                                line_color='#000000',
                                                fill_color='#110000')
                            # mymap.addradpoint(minLat+(((scale - i )+0.5)/normLat),
                            #                  minLon+((j+0.5)/normLon), 30, "#FF0000")

        def plot_timeres(timeres):
            """
            Geo points separated by the time resolution zones
            @return:
            """
            tint = 24/timeres
            step = 255/(tint+1)

            cont = np.zeros((scale, scale))
            for i in range(self.dataset.shape[0]):
                posy = int(((self.dataset[i][0] - minLat) * normLat))
                posx = int(((self.dataset[i][1] - minLon) * normLon))
                if distrib:
                    cont[scale - posy - 1, posx - 1] += 1
                else:
                    cont[scale - posy - 1, posx - 1] = 1
            mxcont = np.max(cont)

            if distrib:
                cont = cont / mxcont
                for i in range(cont.shape[0]):
                    for j in range(cont.shape[1]):
                        if cont[i, j] > 0.01:
                            mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                radius=cont[i,j]*(circlesize/scale),
                                                line_color='#000000',
                                                fill_color='#110000', fill_opacity=0.3)
                            #mymap.addradpoint(minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon),
                            #                  cont[i,j]*(circlesize/scale), "#FF0000")
            else:
                for i in range(cont.shape[0]):
                    for j in range(cont.shape[1]):
                        if cont[i, j] > 0.01:
                            mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                radius=30,
                                                line_color='#000000',
                                                fill_color='#110000', fill_opacity=0.3)
                            #mymap.addradpoint(minLat+(((scale - i )-0.5)/normLat),
                            #                   minLon+((j+1.5)/normLon), 30, "#FF0000")
            for t in range(tint):
                color = '#'+(str(hex((t+1)*step))[2:])+(str(hex((t+1)*step))[2:])+'FF'  # (str(hex((t+1)*step))[2:])
                cont = np.zeros((scale, scale))
                for i in range(self.dataset.shape[0]):
                    posy = int(((self.dataset[i][0] - minLat) * normLat))
                    posx = int(((self.dataset[i][1] - minLon) * normLon))
                    stime = time.localtime(np.int32(self.dataset[i][2]))
                    evtime = stime[3]
                    if (evtime/timeres) == t:
                        if distrib:
                            cont[scale - posy - 1, posx - 1] += 1
                        else:
                            cont[scale - posy - 1, posx - 1] = 1
                if distrib:
                    cont = cont / mxcont
                    for i in range(cont.shape[0]):
                        for j in range(cont.shape[1]):
                            if cont[i, j] > 0.01:
                                mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                   radius=cont[i,j]*(circlesize/scale),
                                                line_color=color,
                                                fill_color='#110000', fill_opacity=0.2)
                else:
                    for i in range(cont.shape[0]):
                        for j in range(cont.shape[1]):
                            if cont[i, j] > 0.01:
                                mymap.circle_marker(location=[minLat+(((scale - i)-0.5)/normLat), minLon+((j+1.5)/normLon)],
                                                    radius=30,
                                                    line_color=color,
                                                    fill_color='#110000', fill_opacity=0.2)

        print 'Generating the events plot ...'
        circlesize = 15000

        # if timeres == 0:
        #     fig = plt.figure()
        #     ax = fig.add_subplot(111)

        minLat, maxLat, minLon, maxLon = self.city[1]
        normLat = scale / (maxLat - minLat)
        normLon = scale / (maxLon - minLon)
        mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1200, height=1000)

#        mymap = pygmaps.maps((minLat+maxLat)/2,(minLon + maxLon)/2.0, 10)
        #mymap.setgrids(minLat, maxLat, 0.01, minLon, maxLon, 0.01)
        if timeres is None:
            plot_notimeres()
        else:
            plot_timeres(timeres)

        #today = time.strftime('%Y%m%d%H%M%S', time.localtime())
        nfile = self.application + '-' + dataname + '-Grid'
        if self.mnhh is not None and self.mnhh is not None:
            nfile += '-nusr' + str(self.mxhh) + '#' + str(self.mnhh)
        if timeres is not None:
            nfile += '-tr' + str(timeres.interval)

        nfile += '-s' + str(scale)

        # if timeres == 0:
        #     fig.savefig(homepath + 'Results/' + self.city[2] + '-' +
        #                 nfile + '.pdf', orientation='landscape', format='pdf')
        #     plt.close()
        mymap.create_map(path=homepath + 'Results/' + self.city[2] + nfile + '.html')
        #mymap.draw(homepath + 'Results/' + self.city[2] + nfile + '.html')


    def plot_events_cluster(self, cluster, distrib=True, dataname='', timeres=None):
        """
        Generates an scale x scale plot of the events
        Every event is represented by a point in the graph
        the ouput is a pdf file and an html file that uses open street maps

        :param int scale: Scale of the spatial discretization
        :param bool distrib: If returns the frequency or the accumulated events
        :param string dataname: Name to append to the filename
        """
        def plot_notimeres():
            """
            All time colapsed
            @return:
            """
            cont = np.zeros(cluster.num_clusters())
            for i in range(self.dataset.shape[0]):
                posy = self.dataset[i][0]
                posx = self.dataset[i][1]
                ejem = np.array([[posy,posx]])
                ncl = cluster.predict(ejem)
                ncl = ncl[0]

                if distrib:
                    cont[ncl] += 1
                else:
                    cont[ncl] = 1

            if distrib:
                cont = cont / np.max(cont)
                for i in range(cont.shape[0]):
                        if cont[i] > 0.01:
                            cx = cluster.cluster_centers_[i][0]
                            cy = cluster.cluster_centers_[i][1]
                            mymap.circle_marker(location=[cx, cy],
                                                radius=cont[i] * circlesize,
                                                line_color='#000000',
                                                fill_color='#110000',
                                                popup=str(cont[i]), fill_opacity=0.4)
            else:
                for i in range(cont.shape[0]):
                        if cont[i] > 0.01:
                            cx = cluster.cluster_centers_[i][0]
                            cy = cluster.cluster_centers_[i][1]

                            mymap.circle_marker(location=[cx,cy],
                                                radius=30,
                                                line_color='#000000',
                                                fill_color='#110000',
                                                popup=str(cont[i]), fill_opacity=0.4)

        def plot_timeres(timeres):
            """
            Geo points separated by the time resolution zones
            @return:
            """
            tint = 24/len(timeres.intervals)
            step = 255/(tint+1)

            cont = np.zeros(cluster.num_clusters())
            for i in range(self.dataset.shape[0]):
                posy = self.dataset[i][0]
                posx = self.dataset[i][1]
                ejem = np.array([[posy, posx]])
                ncl = cluster.predict(ejem)
                ncl = ncl[0]

                if distrib:
                    cont[ncl] += 1
                else:
                    cont[ncl] = 1

            # if distrib:
            #     cont = cont / np.max(cont)
            #     for i in range(cont.shape[0]):
            #         if cont[i] > 0.01:
            #             cx = cluster.cluster_centers_[i][0]
            #             cy = cluster.cluster_centers_[i][1]
            #             mymap.circle_marker(location=[cx, cy],
            #                                 radius=cont[i] * circlesize,
            #                                 line_color='#FF0000',
            #                                 fill_color='#110000')
            # else:
            #     for i in range(cont.shape[0]):
            #         if cont[i] > 0.01:
            #             cx = cluster.cluster_centers_[i][0]
            #             cy = cluster.cluster_centers_[i][1]
            #             mymap.circle_marker(location=[cx, cy],
            #                                 radius=30,
            #                                 line_color='#FF0000',
            #                                 fill_color='#110000')
            for t in range(tint):
                color = '#'+(str(hex((t+1)*step))[2:])+(str(hex((t+1) * step))[2:])+'FF'  # (str(hex((t+1)*step))[2:])
                cont = np.zeros(cluster.num_clusters())
                for i in range(self.dataset.shape[0]):
                    posy = self.dataset[i][0]
                    posx = self.dataset[i][1]
                    ejem = np.array([[posy,posx]])
                    ncl = cluster.predict(ejem)
                    ncl = ncl[0]

                    _, evtime = timeres.discretize(self.dataset[i][2])

                    if evtime == t:
                        if distrib:
                            cont[ncl] += 1
                        else:
                            cont[ncl] = 1
                if distrib:
                    cont = cont / np.max(cont)
                    for i in range(cont.shape[0]):
                            if cont[i] > 0.01:
                                cx = cluster.cluster_centers_[i][0]
                                cy = cluster.cluster_centers_[i][1]
                                mymap.circle_marker(location=[cx, cy],
                                                    radius=cont[i] * circlesize,
                                                    line_color=pltcolors[t],
                                                    fill_color=pltcolors[t],#'#110000',
                                                    popup=str(t) + '-' + str(cont[i]), fill_opacity=0.2)
                else:
                    for i in range(cont.shape[0]):
                        for j in range(cont.shape[1]):
                            if cont[i] > 0.01:
                                cx = cluster.cluster_centers_[i][0]
                                cy = cluster.cluster_centers_[i][1]
                                mymap.circle_marker(location=[cx, cy],
                                                    radius=30,
                                                    line_color=pltcolors[t],
                                                    fill_color=pltcolors[t],#'#110000',
                                                    popup=str(t) + '-' + str(cont[i]), fill_opacity=0.2)

        print 'Generating the events plot ...'
        circlesize = 60000 * cluster.radius

        # if timeres == 0:
        #     fig = plt.figure()
        #     ax = fig.add_subplot(111)

        minLat, maxLat, minLon, maxLon = self.city[1]
        # normLat = scale / (maxLat - minLat)
        # normLon = scale / (maxLon - minLon)
        mymap = folium.Map(location=[(minLat+maxLat)/2.0, (minLon + maxLon)/2.0], zoom_start=12, width=1200, height=1000)

        if timeres is None:
            plot_notimeres()
        else:
            plot_timeres(timeres)

        #today = time.strftime('%Y%m%d%H%M%S', time.localtime())
        nfile = self.application + '-' + dataname + '-Clust'
        if self.mnhh is not None and self.mnhh is not None:
            nfile += '-nusr' + str(self.mxhh) + '#' + str(self.mnhh)

        if timeres is not None:
            nfile += '-tr' + str(timeres.intervals)
        nfile += '-s' + str(cluster.radius)

        # if timeres == 0:
        #     fig.savefig(homepath + 'Results/' + self.city[2] + '-' +
        #                 nfile + '.pdf', orientation='landscape', format='pdf')
        #     plt.close()
        mymap.create_map(path=homepath + 'Results/clusters/' + self.city[2] + nfile + '.html')

    def grid_events(self, scale, threshold=100, distrib=False, dataname=''):
        """
        Generates a plot of the events as a grid

        @param scale:
        @param distrib:
        @param dataname:
        @return:
        """
        def plot_notimeres(thres):
            """
            All time colapsed
            @return:
            """
            cont = np.zeros((scale, scale))
            for i in range(self.dataset.shape[0]):
                posx = int(((self.dataset[i][1] - minLon) * normLon))
                posy = int(((self.dataset[i][0] - minLat) * normLat))

                cont[posx - 1, posy - 1] += 1

            lgeo = []

            for i in range(cont.shape[0]):
                for j in range(cont.shape[1]):
                    if cont[i, j] >= thres:
                        path = [(minLon + (i+0.5)/normLon, maxLat - (scale-j-1.5)/normLat),
                                (minLon + (i+0.5)/normLon, maxLat - (scale-j-0.5)/normLat),
                                (minLon + (i+1.5)/normLon, maxLat - (scale-j-0.5)/normLat),
                                (minLon + (i+1.5)/normLon, maxLat - (scale-j-1.5)/normLat)
                               ]
                        lgeo.append(Feature(geometry=Polygon([path])))

            return lgeo
        minLat, maxLat, minLon, maxLon = self.city[1]
        normLat = scale / (maxLat - minLat)
        normLon = scale / (maxLon - minLon)
        mymap = folium.Map(location=[(minLat+maxLat)/2.0,(minLon + maxLon)/2.0], zoom_start=12, width=1400, height=1000)
        lgeog = plot_notimeres(threshold)

        nfile = self.application + '-' + dataname
        if self.mnhh is not None and self.mnhh is not None:
            nfile += '-nusr' + str(self.mxhh) + '-' + str(self.mnhh)
        nfile += '-s' + str(scale)
        nfile += '-tr' + str(threshold)

        geoc = FeatureCollection(lgeog)
        dump = geojson.dumps(geoc)
        jsfile = open(homepath + 'Results/' + nfile + '.json', 'w')
        jsfile.write(dump)
        jsfile.close()
        mymap.geo_json(geo_path=homepath + 'Results/'+ nfile + '.json', fill_opacity=0.2)

        mymap.create_map(path=homepath + 'Results/' + self.city[2] + nfile + '.html')

    def generate_user_dict(self):
        res={}
        for i in range(self.dataset.shape[0]):
            if self.dataset[i][3].strip() not in res:
                res[self.dataset[i][3].strip()] = 1
            else:
                res[self.dataset[i][3].strip()] += 1
        return res