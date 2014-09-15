# -*- coding: utf-8 -*-
"""
.. module:: Descriptive

Descriptive
************

:Description: SuperHub Descriptive data functions

Functions for computing descriptive statistics from the dataset

For now mainly histograms

:Authors:
    bejar

:Version: 1.0


:File: Descriptive

:Created on: 20/02/2014 15:23


"""

__author__ = 'bejar'

import time

import numpy as np

from Plots import saveHisto, savePlot
from Constants import homepath
from STData import STData
from Transactions import DailyTransactions, DailyDiscretizedTransactions


def plot_accumulated_events(data, distrib=True, scale=100):
    """
    Plots the accumulated geographical events in the selected area to the
    specified scale

    :param: application: name of the data file
    :param: distrib: whether the PDF or the absolute numbers are plotted
    :param: scale: scale of the discretization
    """
    data.contingency(scale, distrib)


def data_histograms(data, lhh=None):
    """
    Generate histograms for different characteristics of the data
    Outputs the data used to generate the histograms

    * Number of daily events
    * Number of days of users (prevalence)
    * Accumulated events per hour
    * Accumulated events per weekday
    * Accumulated events per month

    :param: application:
    :param: lhh:
    """
    if not lhh:
        lhh = [(5, 100)]
    application = data.application
    city = data.city[2]
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    homepathr = homepath + 'Results/'
    for mxhh, mnhh in lhh:
        nfile = '-nusr' + str(mxhh) + '#' + str(mnhh) + '-ts' + today
        data.select_heavy_hitters(mxhh, mnhh)

        print 'Computing daily length histogram'
        transactions = DailyTransactions(data)

        fr = transactions.users_daily_length()

        saveHisto(fr, max(fr), homepathr + city + '-' + application + '-length' + nfile + '.pdf')
        np.savetxt(homepathr + city + '-' + application + '-length' + nfile + '.csv', fr, fmt='%d')

        print 'Computing prevalence histogram'
        fr = transactions.users_prevalence()

        saveHisto(fr, max(fr), homepathr + city + '-' + application + '-prevalence' + nfile + '.pdf')
        np.savetxt(homepathr + city + '-' + application + '-prevalence' + nfile + '.csv', fr, fmt='%d')

        print 'Computing hourly histogram'
        ht = data.hourly_table()

        savePlot(range(24), ht, homepathr + city + '-' + application + '-hourly' + nfile + '.pdf')
        np.savetxt(homepathr + city + '-' + application + '-hourly' + nfile + '.csv',
                   np.array([range(1,25), np.array(ht) / float(np.sum(ht))]).transpose(), fmt='%f')

        print 'Computing daily histogram'
        ht = data.daily_table()

        savePlot(range(7), ht, homepathr + city + '-' + application + '-daily' + nfile + '.pdf')
        np.savetxt(homepathr + city + '-' + application + '-daily' + nfile + '.csv',
                   np.array([range(1,8), np.array(ht) / float(np.sum(ht))]).transpose(), fmt='%f')

        print 'Computing montly histogram'
        ht = data.monthly_table()

        savePlot(range(12), ht, homepathr + city + '-' + application + '-monthy' + nfile + '.pdf')
        np.savetxt(homepathr + city + '-' + application + '-monthly' + nfile + '.csv',
                   np.array([range(1,13), np.array(ht) / float(np.sum(ht))]).transpose(), fmt='%f')


def user_events_histogram(data,  lhh=[0,20000], scale=100, timeres=4):
    """
    Histogram of the number of places-time a user has been

    :param: data: STData
    :param: scale: Discretization scale
    :param: timeres: Time resolution in number of segments from the 24h period
    """
    application = data.application
    mxhh=lhh[0]
    mnhh=lhh[1]
    data.select_heavy_hitters(mxhh, mnhh)
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nfile = application + '-allgeotime' + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-s' + str(scale) \
            + '-tr' + str(int(timeres)) + '-ts' + today

    transactions = DailyDiscretizedTransactions(data, scale=scale, timeres=timeres)
    ctrans = transactions.colapse()

    # number of different geo-time events
    hvals = [len(v) for v in ctrans]
    mxvals = max(hvals)

    saveHisto(hvals, mxvals, homepath + 'Results/' + nfile + '.pdf')

    np.savetxt(homepath + 'Results/' + nfile + '.csv', np.array(hvals).transpose(), fmt='%d')


