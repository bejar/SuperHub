# -*- coding: utf-8 -*-
"""
.. module:: SuperHubProcessing

SuperHubProcessing
************

:Description: SuperHub data processing functions

    Generates different plots from the data

:Authors:
    bejar

:Version: 1.0


"""
__author__ = 'bejar'

import operator
import time

import matplotlib.pyplot as plt

from SuperHubTransactions import dailyTransactions
from SuperHub.Plots import saveHisto, savePlot, plotHisto
from SuperHub.Constants import cpath, minLon, minLat, maxLon, maxLat
from SuperHub.Data import Data
from SuperHub.Transactions import DailyTransactions, DailyDiscretizedTransactions




#from fp_growth import find_frequent_itemsets
from fim import fpgrowth
import numpy as np


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
    Histograms for different characteristics of the data

    * Number of daily events
    * Number of days of users
    * Accumulated events per hour
    * Accumulated ecents per weekday

    :param: application:
    :param: lhh:
    """
    if not lhh: lhh = [(5, 100)]
    data = Data(cpath, application)
    data.read_data()
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    for mxhh, mnhh in lhh:
        nfile = '-nusr' + str(mxhh) + '#' + str(mnhh) + '-ts' + today
        data.select_heavy_hitters(mxhh, mnhh)

        print 'Computing daily length histogram'
        transactions = DailyTransactions(data)

        fr = transactions.users_daily_length()

        saveHisto(fr, max(fr), cpath + application + '-length' + nfile + '.pdf')
        np.savetxt(cpath + application + '-length' + nfile + '.csv', fr)

        print 'Computing prevalence histogram'
        fr = transactions.users_prevalence()

        saveHisto(fr, max(fr), cpath + application + '-prevalence' + nfile + '.pdf')
        np.savetxt(cpath + application + '-prevalence' + nfile + '.csv', fr)

        print 'Computing hourly histogram'
        ht = data.hourly_table()

        savePlot(range(24), ht, cpath + application + '-hourly' + nfile + '.pdf')
        np.savetxt(cpath + application + '-hourly' + nfile + '.csv',
                   np.array([range(24), np.array(ht) / float(np.sum(ht))]).transpose())

        print 'Computing daily histogram'
        ht = data.daily_table()

        savePlot(range(7), ht, cpath + application + '-daily' + nfile + '.pdf')
        np.savetxt(cpath + application + '-daily' + nfile + '.csv',
                   np.array([range(7), np.array(ht) / float(np.sum(ht))]).transpose())

        print 'Computing daily histogram'
        ht = data.monthly_table()

        savePlot(range(12), ht, cpath + application + '-daily' + nfile + '.pdf')
        np.savetxt(cpath + application + '-daily' + nfile + '.csv',
                   np.array([range(12), np.array(ht) / float(np.sum(ht))]).transpose())


def event_histograms(application, mxhh, mnhh):
    """
    Histograms of daily event length and user persistence over time

    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    transactions = dailyTransactions(application, mxhh, mnhh)
    #pp.pprint(transactions)

    fr = []
    for user in transactions:
        usertrans = transactions[user]
        for day in usertrans:
            userdaytrans = usertrans[day]
            fr.append(len(userdaytrans))

    plotHisto(fr, max(fr))

    fr = []
    for user in transactions:
        fr.append(len(transactions[user]))

    plotHisto(fr, max(fr))


def hourly_histogram(data):
    """
    Plots of events accumulated by hours

    """
    ht = data.hourlyTable()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.plot(range(24), ht)
    plt.show()


def daily_histogram(data):
    """
    Plot of events accumulated by week day

    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    ht = data.daily_table()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.plot(range(7), ht)
    plt.show()


def montly_histogram(data):
    """
    Plots the events accumulated by month

    @param application:
    @param mxhh:
    @param mnhh:
    @return:
    """
    ht = data.monthly_table()

    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.plot(range(12), ht)
    plt.show()


def item_key_sort(v):
    """
    auxiliary function for sorting geo-time events

    :param: v:
    :return:
    """
    _, _, h = v.split('#')
    return h


def diff_items(seq):
    """
    Number of different geo point in a sequence

    :param: seq:
    :return:
    """
    tset = set()
    for s in seq:
        x1, y1, _ = s.split('#')
        tset.add(str(x1) + '#' + str(y1))
    return len(tset)


def transaction_routes(data, nfile, scale=100, supp=30, timeres=4.0, colapsed=False):
    """
    Diagram of the routes obtained by the frequent itemsets fp-growth algorithm

    :param: dataclean:
    :param: application:
    :param: mxhh:
    :param: mnhh:
    :param: scale:
    :param: supp:
    :param: timeres:
    """
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nfile = nfile + '-sr' + str(scale) + '-tr' + str(int(timeres)) + '-sp' + str(supp) + '-ts' + today
    if colapsed:
        nfile += '-c'
    rfile = open(cpath + nfile + '.txt', 'w')
    userEvents = DailyDiscretizedTransactions(data, scale=scale, timeres=timeres)

    print 'Serializing the transactions'
    if not colapsed:
        trans = userEvents.serialize()
    else:
        trans = userEvents.colapse()
    print 'Transactions', len(trans)
    ltrans = []
    print 'Applying fp-growth'
    for itemset, sval in fpgrowth(trans, supp=-supp, min=2, target='m'):
        if diff_items(itemset) > 1:
            ltrans.append(itemset)
            print itemset, sval
            rfile.write(str(sorted(itemset, key=item_key_sort)) + ' ' + str(sval) + '\n')

    print 'Routes', len(ltrans)
    fig = plt.figure()

    ax = fig.add_subplot(111)

    cont = np.zeros((scale, scale))

    print 'Generating plot'
    normLat = scale / (maxLat - minLat)
    normLon = scale / (maxLon - minLon)
    dataset = data.get_dataset()
    for i in range(dataset.shape[0]):
        posy = int(((dataset[i][0] - minLat) * normLat))
        posx = int(((dataset[i][1] - minLon) * normLon))
        cont[posy - 1, posx - 1] = 1
    for i in range(cont.shape[0]):
        for j in range(cont.shape[1]):
            if cont[i, j] == 1:
                plt.plot(j, i, 'k.')

    col = ['r-', 'g-', 'b-', 'y-', 'r-', 'g-', 'b-', 'y-']
    for t in ltrans:
        seq = []
        for i in t:
            x, y, h = i.split('#')
            seq.append((x, y, h))
        seqs = sorted(seq, key=operator.itemgetter(2))
        #print seqs
        for p1 in range(len(seqs) - 1):
            x1, y1, _ = seqs[p1]
            x2, y2, _ = seqs[p1 + 1]
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            plt.plot([x1, x2], [y1, y2], col[p1])
            #plt.arrow(x1,y1,x2-x1,y2-y1,fc="r", ec="r")

    #plt.show()
    print nfile
    fig.savefig(cpath + nfile + '.pdf', orientation='landscape', format='pdf')
    rfile.close()


def transaction_routes_many(application, lhh=None, lscale=None, supp=30, ltimeres=None, colapsed=False):
    """
    Computes the diagrams of frequent routes for a list of parameters

    :param: application:
    :param: lhh:
    :param: lscale:
    :param: supp:
    :param: ltimeres:
    """
    if not ltimeres: ltimeres = [4.0]
    if not lscale: lscale = [100]
    if not lhh: lhh = [(5, 100)]
    data = Data(cpath, application)
    data.read_data()
    for mxhh, mnhh in lhh:
        nfile = application + '-routes' + '-nusr' + str(mxhh) + '#' + str(mnhh)
        data.select_heavy_hitters(mxhh, mnhh)
        for scale in lscale:
            for timeres in ltimeres:
                transaction_routes(data, nfile, scale=scale, supp=supp, timeres=timeres, colapsed=colapsed)
    print 'Done.'


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

    # for v in transactions:
    #     print v, transactions[v]
    # number of different geo-time events
    hvals = [len(v) for v in ctrans]
    mxvals = max(hvals)

    saveHisto(hvals, mxvals, cpath + nfile + '.pdf')

    np.savetxt(cpath + nfile + '.csv', np.array(hvals).transpose())



