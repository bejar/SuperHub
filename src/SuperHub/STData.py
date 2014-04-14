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

from Constants import minLat, maxLat, minLon, maxLon, homepath


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

    def read_data(self):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        fname = self.wpath + 'Data/' + self.city + '-' +self.application + '.csv.bz2'
        self.dataset = loadtxt(fname, skiprows=1,
                               dtype=[('lat', 'f8'), ('lng', 'f8'), ('time', 'i32'), ('user', 'S20')],
                               usecols=(0, 1, 2, 3), delimiter=';', comments='#')

    def compute_heavy_hitters(self, mxhh, mnhh):
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
        data = STData(self.wpath, self.application)
        data.dataset = self.dataset[asel]
        data.mxhh = self.mxhh
        data.mnhh = self.mnhh
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

        fig.savefig(homepath + 'Results/' + nfile + '.pdf', orientation='landscape',format='pdf')

        #plt.show()

    def plot_events(self, scale, distrib=True, dataname=''):
        """
        Generates an scale x scale plot of the events
        Every event is represented by a point in the graph

        :param int scale: Scale of the spatial discretization
        :param bool distrib: If returns the frequency or the accumulated events
        :param string dataname: Name to append to the filename
        """
        print 'Generating the events plot ...'
        fig = plt.figure()

        ax = fig.add_subplot(111)

        cont = np.zeros((scale, scale))

        normLat = scale / (maxLat - minLat)
        normLon = scale / (maxLon - minLon)
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
        else:
            for i in range(cont.shape[0]):
                for j in range(cont.shape[1]):
                    if cont[i, j] != 0:
                         plt.plot(j, scale - i, 'k.')
        today = time.strftime('%Y%m%d%H%M%S', time.localtime())
        nfile = self.application + '-' + dataname
        if self.mnhh is not None and self.mnhh is not None:
            nfile += '-nusr' + str(self.mxhh) + '#' + str(self.mnhh)
        nfile += '-s' + str(scale) + '-ts' + today
        fig.savefig(homepath + 'Results/' + nfile + '.pdf', orientation='landscape', format='pdf')

    def generate_user_dict(self):
        res={}
        for i in range(self.dataset.shape[0]):
            if self.dataset[i][3].strip() not in res:
                res[self.dataset[i][3].strip()]=1
            else:
                res[self.dataset[i][3].strip()]+=1
        return res