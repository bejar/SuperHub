# -*- coding: utf-8 -*-
"""
.. module:: SuperHubConstants

Constants
************

:Description: SuperHub constants,

    The coordinates of the region of interest and the path to the data files
    And the information of the mongo database

:Authors:
    bejar

:Version: 1.0


"""

__author__ = 'bejar'

from Parameters.Pconstants import mgdbbcn, mgdbmilan, mgdbhelsinki

homepath = '/home/bejar/Data/SuperHub/'

# 45.467 9.200
bcncoord = (41.24, 41.59, 1.95, 2.34)
milancoord = (45.33, 45.59, 9.03, 9.37)
hlsnkcoord = (60.02, 60.30, 24.72, 25.10)
pariscoord = (48.52, 49.05, 1.97, 2.68)
londoncoord = (51.23, 51.8, -0.50, 0.37)
berlincoord = (52.32, 52.62, 13.11, 13.60)
romecoord = (41.78, 42.0, 12.33, 12.62)
bcnigcircles = [(41.40, 2.14), (41.46, 2.20), (41.33, 2.07), (41.445, 2.03)]
parisigcircles = [(48.65, 2.33), (48.75, 2.33), (48.85, 2.33), (48.95, 2.33), (49.05, 2.33),
            (48.8, 2.45), (48.9, 2.45), (49, 2.45), (48.7, 2.45),
            (48.8, 2.21), (48.9, 2.21), (49, 2.21), (48.7, 2.21),
            (48.65, 2.09), (48.75, 2.09), (48.85, 2.09), (48.95, 2.09), (49.05, 2.09),
            (48.65, 2.57), (48.75, 2.57), (48.85, 2.57), (48.95, 2.57), (49.05, 2.57)]
londonigcircles = [(51.31, -0.07), (51.41, -0.07), (51.51, -0.07), (51.61, -0.07), (51.71, -0.07),
                   (51.35, 0.05), (51.45, 0.05), (51.55, 0.05), (51.65, 0.05),
                   (51.35, -0.19), (51.45, -0.19), (51.55, -0.19), (51.65, -0.19),
                   (51.31, -0.31), (51.41, -0.31), (51.51, -0.31), (51.61, -0.31), (51.71, -0.31),
                   (51.35, -0.43), (51.45, -0.43), (51.55, -0.43), (51.65, -0.43),
                   (51.41, 0.17), (51.51, 0.17), (51.61, 0.17),
                   (51.41, -0.55), (51.51, -0.55), (51.61, -0.55)]
romeigcircles = [(41.85, 12.49), (41.95, 12.49), (41.75, 12.49),
                 (41.80, 12.59), (41.90, 12.59), (41.85, 12.70),
                 (41.80, 12.39), (41.90, 12.39), (41.80, 12.29)]
berlinigcircles = [(52.52, 13.40), (52.62, 13.40), (52.42, 13.40),
                   (52.47, 13.30), (52.57, 13.30), (52.37, 13.30),
                   (52.47, 13.50), (52.57, 13.50), (52.37, 13.50),
                   (52.52, 13.60), (52.42, 13.60),
                   (52.52, 13.20), (52.42, 13.20)]
milanigcircles = [(45.46, 9.18), (45.56, 9.18), (45.36, 9.18),
                  (45.51, 9.28), (45.41, 9.28),
                  (45.51, 9.08), (45.41, 9.08)]

bcnparam = (mgdbbcn, bcncoord, 'bcn', bcnigcircles, 300)
milanparam = (mgdbmilan, milancoord, 'milan', milanigcircles, 300)
hlsnkparam = (mgdbhelsinki, hlsnkcoord, 'hlsnk')
parisparam = (None, pariscoord, 'paris', parisigcircles, 180)
londonparam = (None, londoncoord, 'london', londonigcircles, 180)
berlinparam = (None, berlincoord, 'berlin', berlinigcircles, 300)
romeparam = (None, romecoord, 'rome', romeigcircles, 300)

cityparams ={
    'bcn': bcnparam,
    'milan': milanparam,
    'paris': parisparam,
    'london': londonparam,
    'berlin': berlinparam,
    'rome': romeparam
}

TW_TIMEOUT = 3600 # 1 hour
IG_TIMEOUT = 300 # 5 minutes