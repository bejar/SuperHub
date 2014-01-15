# -*- coding: utf-8 -*-
"""
.. module:: SuperHubPlot

SuperHubPlot
************

:Description: Different plots of the data

:Authors:
    bejar

:Version: 1.0


"""

__author__ = 'bejar'

import matplotlib.pyplot as plt
import pylab
from SuperHubConstants import minLat, maxLat, minLon, maxLon
import matplotlib.cm as cm
import numpy as np


def plotHisto(data, bins):
    """
    Plots a histogram

    :param: data:
    :param: bins:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(data, bins=bins,
                               normed=True, facecolor='green', alpha=0.75)

    ax.set_xlabel('Freqs')
    #    ax.set_xlim(min(data), 1500)
    #    ax.set_ylim(0, 0.1)
    ax.grid(True)
    plt.show()


def saveHisto(data, bins, fname):
    """
    Saves a histogram

    :param: data:
    :param: bins:
    :param: fname:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(data, bins=bins,
                               normed=True, facecolor='green', alpha=0.75)

    ax.set_xlabel('Freqs')
    #    ax.set_xlim(min(data), 1500)
    #    ax.set_ylim(0, 0.1)
    ax.grid(True)
    title= fname.split('/')
    plt.title(title[-1])


    fig.savefig(fname, orientation='landscape', format='pdf')


def savePlot(axis, data, fname):
    """
    Saves a plot of the data using the values of axis

    :param: data:
    :param: num:
    :param: fname:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(axis, data)
    title= fname.split('/')
    plt.title(title[-1])
    fig.savefig(fname, orientation='landscape', format='pdf')


def contingency(data, scale, distrib=True):
    """
    Generates an scale x scale accumulated plot of the events

    :param: data:
    :param: scale:
    :param: distrib:
    """

    cont = np.zeros((scale, scale))
    normLat = scale / (maxLat - minLat)
    normLon = scale / (maxLon - minLon)

    # syn = (index, rel index, class)
    for i in range(data.shape[0]):
        posy = int(((data[i][0] - minLat) * normLat))
        posx = int(((data[i][1] - minLon) * normLon))
#        print posx,posy,data[i][0],data[i][1], normLat, normLon
        try:
            if distrib:
                cont[scale - posy - 1, posx - 1] += 1
            else:
                cont[scale - posy - 1, posx - 1] = 1
        except IndexError:
            print data[i][0], data[i][1]
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

