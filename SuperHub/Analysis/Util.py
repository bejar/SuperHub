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

import string
import time
import numpy as np
import matplotlib.colors as colors

def now():
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def item_key_sort(v):
    """
    auxiliary function for sorting geo-time events using the t

    :param v: item
    :return: time discretization of the item
    """
    _, _, h = v.split('#')
    return h


def diff_items(seq):
    """
    Number of different geo point in a sequence

    :param seq: sequence of ST items
    :return: number of different items in the sequence
    """
    tset = set()
    for s in seq:
        x1, y1, _ = s.split('#')
        tset.add(str(x1) + '#' + str(y1))
    return len(tset)


def item_to_column(item, scale):
    """
    Transforms an item to a column number given the scale of the discretization
    an item is a string with the format posx#posy#time

    :param string item: string corresponding to two coordinates and a time dicretization
    :param int scale: value used in the scaling
    :returns: Integer corresponding to the column of the item
    :rtype: int
    """
    x, y, t = item.split('#')
    return (int(t) * scale * scale) + (int(y) * scale) + int(x)


def strip_nl(val):
    """
    Deletes the CR of the string and deletes leading and trailing spaces
    @param val:
    @return:
    """
    return (string.lstrip(string.rstrip(val[:len(val) - 1])))

def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    # R *= 255
    # G *= 255
    # B *= 255
    return (R, G, B)


def choose_color(nsym):
    """
    selects the  RBG colors from a range with maximum nsym colors
    :param mx:
    :return:
    """
    lcols = []
    for i in  np.arange(380,750,370.0/nsym):
        r,g,b = wavelength_to_rgb(i)
        lcols.append(colors.rgb2hex((r, g, b)))
    return lcols[0:nsym]
