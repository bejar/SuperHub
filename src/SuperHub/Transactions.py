# -*- coding: utf-8 -*-
"""
.. module:: Transactions

Transactions
*************

:Description: Transactions,

    Class for transactions processing

:Authors:
    bejar

:Version: 1.0

:Created on: 18/02/2014 10:59

"""

__author__ = 'bejar'

import time

import numpy as np

from Constants import minLat, maxLat, minLon, maxLon
from Util import item_to_column
from scipy.sparse import coo_matrix
from math import log

class Transactions:
    """
    Class for the user transactions
    :param data: STData
    """
    usertrans = None
    application = None
    wpath = None

    def __init__(self, data):
        self.usertrans = None
        self.application = data.application
        self.wpath = data.wpath


class DailyTransactions(Transactions):
    """
    Class for the daily transactions
    """

    def __init__(self, data):
        """
        Extracts the daily event transactions of the users

        :param data: is a SuperHub Data object
        """
        Transactions.__init__(self, data)
        dataclean = data.dataset
        usertrans = {}
        for i in range(dataclean.shape[0]):
            user = str(int(dataclean[i][3]))
            pos = str(dataclean[i][0]) + '/' + str(dataclean[i][1])
            #        print i, user, pos
            stime = time.localtime(np.int32(dataclean[i][2]))
            evtime = time.strftime('%Y%m%d', stime)
            if not user in usertrans:
                usertrans[user] = {evtime: [pos]}
            else:
                uev = usertrans[user]
                if not evtime in uev:
                    uev[evtime] = [pos]
                else:
                    uev[evtime].append(pos)
        self.usertrans = usertrans

    def serialize(self):
        """
        Transforms the transactions from dictionaries to lists

        :returns: Returns a list representation of the transactions
        """
        trans = self.usertrans
        ltrans = []
        for user in trans:
            usertrans = trans[user]
            for day in usertrans:
                userdaytrans = usertrans[day]
                l = []
                for pos in userdaytrans:
                    l.append(pos)
                ltrans.append(l)
        return ltrans

    def colapse(self):
        """
        Colapses the transactions of a user on a set with all the different items
        in the transactions (basically where has been and when (considering the
        discretization used) during the period of time covered by the transactions

       :returns: Dictionary of daily transactions
        """
        print 'Generating colapsed Transactions ...'
        trans = self.usertrans
        userEvents = []
        for user in trans:
            items = set()
            for day in trans[user]:
                userdaytrans = trans[user][day]
                items = items.union(userdaytrans)
            userEvents.append(list(items))
        return userEvents

    def colapse_count(self):
        """
        Colapses the transactions of a user on a dictionary with all the different items in the
        transactions, counting how many times the user has been at that time at that place (considering
        the discretization used)

        :returns: A dictionary of users with the count of the times they has been in a place/time
        """
        print 'Generating colapsed Transactions ...'
        trans = self.usertrans
        userEvents = {}
        for user in trans:
            items = {}
            for day in trans[user]:
                userdaytrans = trans[user][day]
                for utrans in userdaytrans:
                    if utrans in items:
                        items[utrans] += 1
                    else:
                        items[utrans] = 1
            userEvents[user] = items
        return userEvents

    def save(self, rfile):
        """
        Saves the daily transactions in a file

        :param rfile: File for the output. The function closes the file
        """
        trans = self.usertrans
        for user in trans:
            usertrans = trans[user]
            for day in usertrans:
                userdaytrans = usertrans[day]
                l = []
                for pos in userdaytrans:
                    l.append(pos)
                for i in range(len(l) - 1):
                    rfile.write(l[i] + ',')

                rfile.write(l[len(l) - 1] + '\n')
                rfile.flush()
        rfile.close()

    def users_daily_length(self):
        """
        Computes the list of lengths of the daily transactions for all users

        :returns: A list with the count of events of each the users for each day
        """
        transactions = self.usertrans
        fr = []
        for user in transactions:
            usertrans = transactions[user]
            for day in usertrans:
                userdaytrans = usertrans[day]
                fr.append(len(userdaytrans))
        return fr

    def users_prevalence(self):
        """
        Computes the number of daily transactions for all users

        Used to compute user prevalence histograms

        :returns: list with the count of tractactions for each user
        """
        transactions = self.usertrans
        fr = []
        for user in transactions:
            fr.append(len(transactions[user]))
        return fr


class DailyDiscretizedTransactions(DailyTransactions):
    """
    Class for the daily discretized transactions

    :param data: STData
    :param scale: Space distretization
    :param timeres: Time distretization
    """
    scale = None
    timeres = None

    def __init__(self, data, scale=100, timeres=4):
        """
        Extracts the daily event transactions of the users, discretizing
        the positions to a NxN grid and a time resolution

        :param: data: STData
        :param: scale: Space distretization
        :param: timeres: Time distretization

        """
        self.scale = scale
        self.timeres = timeres
        DailyTransactions.__init__(self, data)
        dataclean = data.dataset
        userEvents = {}
        normLat = scale / (maxLat - minLat)
        normLon = scale / (maxLon - minLon)
        print 'Generating Transactions ...'
        for i in range(dataclean.shape[0]):
            user = str(int(dataclean[i][3]))
            posy = int(((dataclean[i][0] - minLat) * normLat))
            posx = int(((dataclean[i][1] - minLon) * normLon))
            #        print i, user, pos
            stime = time.localtime(np.int32(dataclean[i][2]))
            evtime = time.strftime('%Y%m%d', stime)
            quart = int(stime[3] / timeres)
            pos = str(posx - 1) + '#' + str(posy - 1) + '#' + str(quart)  # Grid position/time
            if not user in userEvents:
                a = set()
                a.add(pos)
                userEvents[user] = {evtime: a}
            else:
                uev = userEvents[user]
                if not evtime in uev:
                    a = set()
                    a.add(pos)
                    uev[evtime] = a
                else:
                    uev[evtime].add(pos)
        self.usertrans = userEvents

    def generate_data_matrix(self, minloc=20, mode='af'):
        """
        Generates a sparse data matrix from the transactions

        :param int minloc: Minimun number of locations for a user
        :param string mode:

         * af = location absolute frequency (total number of times)
         * nf = location normalized frequency for the user (divided by all user locations)
         * bin = presence/non presence of the location

          if the mode includes 'idf' the td x idf value is computed

        :returns: csc sparse numpy array representing the user locations
             and a list of the selected users
        :rtype: csc sparse matrix, list
        """
        print 'Generating data matrix ...'
        trans = self.colapse_count()
        # Computing the idf term
        nd = 0
        idf = {}
        if 'idf' in mode:
            for user in trans:
                if len(trans[user]) > minloc:
                    for tr in trans[user]:
                        if tr in idf:
                            idf[tr] += 1
                        else:
                          idf[tr] = 1
                nd += 1
        for tr in idf:
            idf[tr] = log(nd / idf[tr])
        ## Computing the value
        lcol = []
        lrow = []
        lval = []
        lusers = []
        i = 0
        for user in trans:
            if len(trans[user]) > minloc:
                lusers.append(user)
                lplaces = trans[user]
                if 'nf' in mode:
                    usum = reduce(lambda x, y: x + y, [lplaces[v] for v in lplaces])
                    for tr in lplaces:
                        lcol.append(item_to_column(tr, self.scale))
                        lrow.append(i)
                        if 'idf' in mode:
                            lval.append(lplaces[tr]/float(usum) * idf[tr])
                        else:
                            lval.append(lplaces[tr]/float(usum))
                if 'af' in mode:
                    for tr in lplaces:
                        lcol.append(item_to_column(tr, self.scale))
                        lrow.append(i)
                        if 'idf' in mode:
                            lval.append(lplaces[tr] * idf[tr])
                        else:
                            lval.append(lplaces[tr])
                elif 'bin' in mode:
                    for tr in lplaces:
                        lcol.append(item_to_column(tr, self.scale))
                        lrow.append(i)
                        if 'idf' in mode:
                            lval.append(idf[tr])
                        else:
                            lval.append(1)

                i += 1
        datamat = coo_matrix((np.array(lval), (np.array(lrow), np.array(lcol))), shape=(i, self.scale*self.scale*(24/self.timeres)))
        return datamat.tocsc(), lusers

