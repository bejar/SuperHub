# -*- coding: utf-8 -*-
"""
File: Descriptive

Created on 20/02/2014 15:23

Functions for computing descriptive statistics from the dataset

For now mainly histograms

@author: bejar

"""

__author__ = 'bejar'

import time

import numpy as np

from SuperHub.Plots import saveHisto, savePlot
from Constants import homepath
from SuperHub.Data import Data
from SuperHub.Transactions import DailyTransactions, DailyDiscretizedTransactions


def plot_accumulated_events(data, distrib=True, scale=100):
    """
    Plots the accumulated geographical events in the selected area to the
    specified scale

    :param: application: name of the data file
    :param: distrib: whether the PDF or the absolute numbers are plotted
    :param: scale: scale of the discretization
    """
    data.contingency(scale, distrib)


def data_histograms(application, lhh=None):
    """
    Generate histograms for different characteristics of the data
    Outputs the data used to generate the histograms

    * Number of daily events
    * Number of days of users
    * Accumulated events per hour
    * Accumulated ecents per weekday

    :param: application:
    :param: lhh:
    """
    if not lhh: lhh = [(5, 100)]
    data = Data(homepath, application)
    data.read_data()
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    homepathr = homepath + 'Results/'
    for mxhh, mnhh in lhh:
        nfile = '-nusr' + str(mxhh) + '#' + str(mnhh) + '-ts' + today
        data.select_heavy_hitters(mxhh, mnhh)

        print 'Computing daily length histogram'
        transactions = DailyTransactions(data)

        fr = transactions.users_daily_length()

        saveHisto(fr, max(fr), homepath + application + '-length' + nfile + '.pdf')
        np.savetxt(homepathr + application + '-length' + nfile + '.csv', fr)

        print 'Computing prevalence histogram'
        fr = transactions.users_prevalence()

        saveHisto(fr, max(fr), homepath + application + '-prevalence' + nfile + '.pdf')
        np.savetxt(homepath + application + '-prevalence' + nfile + '.csv', fr)

        print 'Computing hourly histogram'
        ht = data.hourly_table()

        savePlot(range(24), ht, homepath + application + '-hourly' + nfile + '.pdf')
        np.savetxt(homepathr + application + '-hourly' + nfile + '.csv',
                   np.array([range(24), np.array(ht) / float(np.sum(ht))]).transpose())

        print 'Computing daily histogram'
        ht = data.daily_table()

        savePlot(range(7), ht, homepath + application + '-daily' + nfile + '.pdf')
        np.savetxt(homepathr + application + '-daily' + nfile + '.csv',
                   np.array([range(7), np.array(ht) / float(np.sum(ht))]).transpose())

        print 'Computing daily histogram'
        ht = data.monthly_table()

        savePlot(range(12), ht, homepath + application + '-daily' + nfile + '.pdf')
        np.savetxt(homepathr + application + '-daily' + nfile + '.csv',
                   np.array([range(12), np.array(ht) / float(np.sum(ht))]).transpose())


def user_events_histogram(data, scale=100, timeres=4):
    """
    Histogram of the number of places-time a user has been

    :param: scale:
    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    application = data.application
    mxhh = data.mxhh
    mnhh = data.mnhh

    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nfile = application + '-allgeotime' + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-s' + str(scale) \
            + '-tr' + str(int(timeres)) + '-ts' + today

    transactions = DailyDiscretizedTransactions(data, scale=scale, timeres=timeres)
    ctrans = transactions.colapse()

    # number of different geo-time events
    hvals = [len(v) for v in ctrans]
    mxvals = max(hvals)

    saveHisto(hvals, mxvals, homepath + 'Results/' + nfile + '.pdf')

    np.savetxt(homepath + nfile + '.csv', np.array(hvals).transpose())


