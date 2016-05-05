"""
.. module:: SuperHub.Plot

Plot
************

:Description: Different plots of the data

:Authors:
    bejar

:Version: 1.0

"""

__author__ = 'bejar'

import matplotlib.pyplot as plt


def plotHisto(data, bins):
    """Plots a histogram

    :param: data:
    :param: bins:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(data, bins=bins,
                               normed=True, facecolor='green', alpha=0.75)

    ax.set_xlabel('Freqs')
    # ax.set_xlim(min(data), 1500)
    #    ax.set_ylim(0, 0.1)
    ax.grid(True)
    plt.show()


def saveHisto(data, bins, fname):
    """Saves a histogram

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
    # ax.set_xlim(min(data), 1500)
    #    ax.set_ylim(0, 0.1)
    ax.grid(True)
    title = fname.split('/')
    plt.title(title[-1])

    fig.savefig(fname, orientation='landscape', format='pdf')
    plt.close()


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
    title = fname.split('/')
    plt.title(title[-1])
    fig.savefig(fname, orientation='landscape', format='pdf')
    plt.close()


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

