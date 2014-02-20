# -*- coding: utf-8 -*-
"""
File: Transactions

Created on 18/02/2014 10:59 

@author: bejar

"""

__author__ = 'bejar'

import time

import numpy as np

from Constants import minLat, maxLat, minLon, maxLon


class Transactions:
    """
    Class for the user transactions
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

            :param: data is a SuperHub Data object
            :return:
            """
        Transactions.__init__(self, data)
        dataclean = data.get_dataset()
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

        :param: trans:
        :return:
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

        :param: trans: Dictionary of user/time transactions
        :return: Dictionary of daily transactions
        """
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
        Colapsed the transactions of a user on a dictionary with all the different items in the
        transctions, counting how many times the user has been at that time at that place (considering
        the discretization used)
        @return:
        """
        trans = self.usertrans
        userEvents = []
        for user in trans:
            items = {}
            for day in trans[user]:
                userdaytrans = trans[user][day]
                if userdaytrans in items:
                    items[userdaytrans] += 1
                else:
                    items[userdaytrans] = 1
            userEvents.append(items)
        return userEvents


    def save(self, rfile):
        """
        Saves the daily transactions in a file

        :param: nfile:
        :param: application:
        :param: mxhh:
        :param: mnhh:
        :param: scale:
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
        """
        transactions = self.usertrans
        fr = []
        for user in transactions:
            fr.append(len(transactions[user]))
        return fr


class DailyDiscretizedTransactions(DailyTransactions):
    """
    Class for the daily discretized transactions
    """

    def __init__(self, data, scale=100, timeres=4.0):
        """
            Extracts the daily event transactions of the users, discretizing
            the positions to a NxN grid and a time resolution

            :param: application:
            :param: scale:
            :return:
            @param data:
            @param scale:
            @param timeres:
            """
        DailyTransactions.__init__(self, data)
        dataclean = data.get_dataset()
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
            pos = str(posx - 1) + '#' + str(posy - 1) + '#' + str(quart)  # Grid position
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
