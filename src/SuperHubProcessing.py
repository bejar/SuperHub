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
from SuperHubData import computeHeavyHitters, selectDataUsers, readData, hourlyTable, dailyTable,  cleanDataArea
from SuperHubTransactions import dailyTransactions, serializeDailyTransactions, dailyDiscretizedTransactions
from SuperHubTransactions import colapseUserDailyTransactions
from SuperHubPlot import saveHisto, savePlot, contingency, plotHisto
from SuperHubConstants import cpath, minLon, minLat, maxLon, maxLat
import time
import matplotlib.pyplot as plt

#from fp_growth import find_frequent_itemsets
from fim import fpgrowth
import numpy as np

def accumulatedEvents(application, distrib=True, scale=100):
    """
    Plots the accumulated geographical events in the selected area to the
    specified scale

    :param: application: name of the data file
    :param: distrib: whether the PDF or the absolute numbers are plotted
    :param: scale: scale of the discretization
    """
    print 'Reading Data ...'
    dataclean = readData(application)
    #dataclean = cleanDataArea(data)
    print dataclean.shape
    print 'Generating the plot ...'
    contingency(dataclean, scale, distrib)


def dataHistograms(application, lhh=None):
    """
    Histograms for different characteristics of the data

    :param: application:
    :param: lhh:
    """
    if not lhh: lhh = [(5, 100)]
    print 'Reading Data'
    data = readData(application)
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    for mxhh, mnhh in lhh:
        nfile = '-nusr' + str(mxhh) + '#' + str(mnhh) + '-ts' + today
        print 'Computing Heavy Hitters'
        lhh = computeHeavyHitters(data, mxhh, mnhh)
        print 'Selecting Heavy Hitters'
        dataclean = selectDataUsers(data, lhh)

        print 'Computing daily length histogram'
        transactions = dailyTransactions(application, mxhh, mnhh)

        fr = []
        for user in transactions:
            usertrans = transactions[user]
            for day in usertrans:
                userdaytrans = usertrans[day]
                fr.append(len(userdaytrans))

        saveHisto(fr, max(fr), cpath + application + '-length' + nfile + '.pdf')

        print 'Computing prevalence histogram'
        fr = []
        for user in transactions:
            fr.append(len(transactions[user]))

        saveHisto(fr, max(fr), cpath + application + '-prevalence' + nfile + '.pdf')

        print 'Computing hourly histogram'
        ht = hourlyTable(dataclean)

        savePlot(range(24), ht, cpath + application + '-hourly' + nfile + '.pdf')

        print 'Computing daily histogram'
        ht = dailyTable(dataclean)

        savePlot(range(7), ht, cpath + application + '-hourly' + nfile + '.pdf')



def eventHistograms(application, mxhh, mnhh):
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


def accumulatedEventsHeavyHitters(application, mxhh, mnhh, distrib=True, scale=100):
    """
    Plots accumulated geografical events for heavy hitters

    :param: application:
    :param: mxhh:
    :param: mnhh:
    :param: distrib:
    :param: scale:
    """
    data = readData(application)
    dataclean = selectDataUsers(data, computeHeavyHitters(data, mxhh, mnhh))
    print dataclean.shape
    contingency(dataclean, scale, distrib)


def hourlyHistogram(application, mxhh, mnhh):
    """

    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    data = readData(application)
    dataclean = selectDataUsers(data, computeHeavyHitters(data, mxhh, mnhh))
    ht = hourlyTable(dataclean)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.plot(range(24), ht)
    plt.show()


def dailyHistogram(application, mxhh, mnhh):
    """
    Plot of events accumulated by week day

    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    data = readData(application)
    dataclean = selectDataUsers(data, computeHeavyHitters(data, mxhh, mnhh))
    ht = dailyTable(dataclean)

    fig = plt.figure()

    ax = fig.add_subplot(111)
    plt.plot(range(7), ht)
    plt.show()


def itemkeysort(v):
    """
    auxiliary function for sorting geo-time events

    :param: v:
    :return:
    """
    _, _, h = v.split('#')
    return h


def diffItems(seq):
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


#def transactionRoutes(dataclean, application, mxhh, mnhh, scale=100, supp=30, timeres=4.0):
def transactionRoutes(dataclean, nfile, scale=100, supp=30, timeres=4.0):
    """
    Diagram of the routes obtained by the frequent itemsets fp-.growth algorithm

    :param: dataclean:
    :param: application:
    :param: mxhh:
    :param: mnhh:
    :param: scale:
    :param: supp:
    :param: timeres:
    """
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nfile = nfile + '-s' + str(scale) + '-sp' + str(supp) + 'tr' + str(
        int(timeres)) + '-ts' + today
    rfile = open(cpath + nfile + '.txt', 'w')
    userEvents= dailyDiscretizedTransactions(dataclean, scale=scale, timeres=timeres)

    print 'Serializing the transactions'
    trans = serializeDailyTransactions(userEvents)
    print 'Transactions', len(trans)
    ltrans = []
    print 'Applying fp-growth'
    for itemset, sval in fpgrowth(trans, supp=-supp, min=2, target='m'):
        if diffItems(itemset) > 1:
            ltrans.append(itemset)
            print itemset, sval
            rfile.write(str(sorted(itemset, key=itemkeysort)) + ' ' + str(sval) + '\n')

    print 'Routes', len(ltrans)
    fig = plt.figure()

    ax = fig.add_subplot(111)

    cont = np.zeros((scale, scale))

    print 'Generating plot'
    normLat = scale / (maxLat - minLat)
    normLon = scale / (maxLon - minLon)
    for i in range(dataclean.shape[0]):
        posy = int(((dataclean[i][0] - minLat) * normLat))
        posx = int(((dataclean[i][1] - minLon) * normLon))
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


def transactionRoutesMany(application, lhh=None, lscale=None, supp=30, ltimeres=None):
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
    print 'Reading Data'
    data = readData(application)
    for mxhh, mnhh in lhh:
        nfile = application + '-routes' + '-nusr' + str(mxhh) + '#' + str(mnhh)
        print 'Computing Heavy Hitters'
        lhh = computeHeavyHitters(data, mxhh, mnhh)
        print 'Selecting Heavy Hitters'
        dataclean = selectDataUsers(data, lhh)
        for scale in lscale:
            for timeres in ltimeres:
                transactionRoutes(dataclean, nfile, scale=scale, supp=supp, timeres=timeres)
    print 'Done.'


def userEventsHistogram(application, mxhh, mnhh, scale=100, timeres=4):
    """
    Histogram of the number of places-time a user has been

    :param: scale:
    :param: application:
    :param: mxhh:
    :param: mnhh:
    """
    today = time.strftime('%Y%m%d%H%M%S', time.localtime())
    nfile = application + '-allgeotime' + '-nusr' + str(mxhh) + '#' + str(mnhh) + '-s' + str(scale) \
            + '-tr' + str(int(timeres)) + '-ts' + today

    transactions = colapseUserDailyTransactions(
        dailyDiscretizedTransactions(application, mxhh, mnhh, scale=scale,timeres=timeres))

    # for v in transactions:
    #     print v, transactions[v]
    # number of different geo-time events
    hvals = [len(transactions[v]) for v in transactions]
    mxvals = max(hvals)

    saveHisto(hvals,mxvals, cpath + nfile + '.pdf')



