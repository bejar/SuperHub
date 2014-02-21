"""
.. module:: Util

Util
******

:Description: Util

    Different Auxiliary functions used for different purposes

:Authors:
    bejar

:Version: 1.0

:File: Util

:Created on: 20/02/2014 14:12
"""

__author__ = 'bejar'


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