# -*- coding: utf-8 -*-
"""
.. module:: Routes

Routes
******

:Description: Routes

    Routines that compute routes

:Authors:
    bejar

:Version: 1.0

:File: Routes

:Created on: 20/02/2014 15:17
r

"""

__author__ = 'bejar'

#from fp_growth import find_frequent_itemsets
from fim import fpgrowth
import time
import operator

import numpy as np
import matplotlib.pyplot as plt

from Constants import homepath
from Transactions import DailyDiscretizedTransactions
from Util import item_key_sort, diff_items


def transaction_routes(data, nfile, scale=100, supp=30, timeres=4.0, colapsed=False):
    """
    Generates a diagram of the routes obtained by the frequent itemsets fp-growth algorithm

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

    # File for the textual results
    rfile = open(homepath + 'Results/' + nfile + '.txt', 'w')
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
    minLat, maxLat, minLon, maxLon = data.city[1]
    normLat = scale / (maxLat - minLat)
    normLon = scale / (maxLon - minLon)
    dataset = data.dataset
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

    # Saving the plot
    fig.savefig(homepath + 'Results/' + nfile + '.pdf', orientation='landscape', format='pdf')
    rfile.close()


def transaction_routes_many(data, lhh=None, lscale=None, supp=30, ltimeres=None, colapsed=False):
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
    application = data.application
    for mxhh, mnhh in lhh:
        nfile = application + '-routes' + '-nusr' + str(mxhh) + '#' + str(mnhh)
        hhdata = data.select_heavy_hitters(mxhh, mnhh)
        for scale in lscale:
            for timeres in ltimeres:
                transaction_routes(hhdata, nfile, scale=scale, supp=supp, timeres=timeres, colapsed=colapsed)
    print 'Done.'

