# -*- coding: utf-8 -*-
"""
.. module:: SuperHubTransactions

SuperHubTransactions
************

:Description: Functions that process events as transactions

:Authors:
    bejar

:Version: 1.0


"""

__author__ = 'bejar'

from SuperHubConstants import minLat, maxLat, minLon, maxLon, cpath
from SuperHubData import computeHeavyHitters, selectDataUsers, readData
import time
import numpy as np


def dailyTransactions(dataclean):
    """
    Extracts the daily event transactions of the users with most events

    :param: application:
    :param: mxhh:
    :param: mnhh:
    :return:
    """

    userEvents = {}
    for i in range(dataclean.shape[0]):
        user = str(int(dataclean[i][3]))
        pos = str(dataclean[i][0]) + '/' + str(dataclean[i][1])
        #        print i, user, pos
        stime = time.localtime(np.int32(dataclean[i][2]))
        evtime = time.strftime('%Y%m%d', stime)
        if not user in userEvents:
            userEvents[user] = {evtime: [pos]}
        else:
            uev = userEvents[user]
            if not evtime in uev:
                uev[evtime] = [pos]
            else:
                uev[evtime].append(pos)
    return userEvents


def dailyDiscretizedTransactions(dataclean, scale=100,timeres=4.0):
    """
    Extracts the daily event transactions of the users with most events
    Discretizing the positions to a NxN grid and a time resolution

    :param: application:
    :param: mxhh:
    :param: mnhh:
    :param: scale:
    :return:
    """
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
        pos = str(posx - 1) + '#' + str(posy - 1) + '#' + str(quart) # Grid position
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
    return userEvents


def serializeDailyTransactions(trans):
    """
    Transforms the transactions from dictionaries to lists

    :param: trans:
    :return:
    """
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


# def colapseUserDailyTransactions(trans):
#     """
#     Colapses the transactions of a user on a set with all the different items
#
#     :param: trans: Dictionary of user/time transactions
#     :return: Dictionary of daily transactions
#     """
#     userEvents = {}
#     for user in trans:
#         items = set()
#         for day in trans[user]:
#             userdaytrans = trans[user][day]
#             items = items.union(userdaytrans)
#         userEvents[user] = items
#     return userEvents


def colapseUserDailyTransactions(trans):
    """
    Colapses the transactions of a user on a set with all the different items

    :param: trans: Dictionary of user/time transactions
    :return: Dictionary of daily transactions
    """
    userEvents = []
    for user in trans:
        items = set()
        for day in trans[user]:
            userdaytrans = trans[user][day]
            items = items.union(userdaytrans)
        userEvents.append(list(items))
    return userEvents


def saveDailyTransactions(nfile, application, mxhh, mnhh, scale=100, timeres=4):
    """
    Saves the daily transactions in a file

    :param: nfile:
    :param: application:
    :param: mxhh:
    :param: mnhh:
    :param: scale:
    """
    rfile = open(cpath + nfile + '.csv', 'w')
    trans = dailyDiscretizedTransactions(application, mxhh, mnhh, scale=scale, timeres=timeres)
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
