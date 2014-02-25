# -*- coding: utf-8 -*-
"""
.. module:: Data

Data
************

:Description: SuperHub Data class

    Performs different processings to the data matrix

:Authors:
    bejar

:Version: 1.0

File: Data

:Created on: 18/02/2014 10:09

"""

__author__ = 'bejar'

import operator
import time

from numpy import loadtxt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from Constants import minLat, maxLat, minLon, maxLon


class Data:
    """
    Class for a superhub dataset

    dataset = numpy array
    application = Name of the data file
    cpath = Path of the data file
    mxhh = maximum position of the heavy hitters list
    mnhh = minimum position of the heavy hitters list
    lhh = list of users ordered by the number of elements in the dataset
    """
    dataset = None
    application = None
    wpath = None
    mxhh = None
    mnhh = None
    lhh = None
    datasethh = None

    def __init__(self,path, application):
        """
        Just sets the path and application for the dataset

        @param path:
        @param application:
        @return:
        """
        self.application = application
        self.wpath = path


    def read_data(self):
        """
        Loads the data from the csv file

        :param: application:
        :return:
        """
        print 'Reading Data ...'
        fname = self.wpath + 'Data/' + self.application + '.csv.bz2'
        self.dataset = loadtxt(fname, skiprows=1, dtype=[('lat', 'f8'), ('lng', 'f8')
            ,('time', 'i32'), ('user', 'S20')], usecols=(0, 1, 2, 3), delimiter=';', comments='#')


    def compute_heavy_hitters(self, mxhh, mnhh):
        """
        Computes the list of the number of events
        and returns a list with the users between the
        positions mxhh and mnhh in the descendent order

        If the list heavy hitters have already been computed it is reused

        :param: data:
        :param: mxhh:
        :param: mnhh:
        :return: list with the list of users
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

        @param mxhh:
        @param mnhh:
        @return: A list of the most active users in the indicated range
        """
        self.mxhh = mxhh
        self.mnhh = mnhh
        lhh = self.compute_heavy_hitters(mxhh, mnhh)
        print 'Selecting Heavy Hitters ...'
        return self.select_data_users(lhh)


    def select_data_users(self, users):
        """
        Selects only the events from the list of users
        Returns a new object with the selected users

        :param: users: List of users to select
        :return:
        """
        print 'Selecting Users ...'
        # First transforms the list of users to a set to be efficient
        susers = set(users)
        # computes the boolean array for the selection
        sel = [self.dataset[i][3] in susers for i in range(self.dataset.shape[0])]
        asel = np.array(sel)
        data = Data(self. wpath, self.application)
        data.dataset = self.dataset[asel]
        return data


    def hourly_table(self):
        """
        Computes the accumulated events by hour for the data table

        :return: An hourly table
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

        :return: A daily table
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

        @return: A montly rable
        """
        htable = [0 for i in range(12)]
        for i in range(self.dataset.shape[0]):
            stime = time.localtime(np.int32(self.dataset[i][2]))
            evtime = stime[1]
            htable[evtime - 1] += 1
        return htable


    def contingency(self, scale, distrib=True):
        """
        Generates an scale x scale accumulated plot of the events

        :param: data:
        :param: scale:
        :param: distrib:
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
                cont = cont / np.sum(cont)

        fig = plt.figure()

        ax = fig.add_subplot(111)
        plt.title('Density ')

        plt.imshow(cont, interpolation='bicubic', cmap=cm.gist_yarg)
        vmax = np.max(cont)
        #    vmin=np.min(cont)

        if distrib:
            plt.colorbar(ticks=np.round(np.linspace(0, 1, 10), 2),
                         orientation='vertical')

        #    fig.savefig(cpath+'/contingency'+str(nsync)+'.pdf', orientation='landscape',format='pdf')

        plt.show()


    def get_dataset(self):
        """
        Returns the numpy array that represents the dataset
        @return:

        """
        return self.dataset