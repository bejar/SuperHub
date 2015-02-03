"""
.. module:: testing

testing
*************

:Description: testing

    

:Authors: bejar
    

:Version: 

:Created on: 15/09/2014 13:03 

"""

__author__ = 'bejar'

import time

from Analysis import TimeDiscretizer


d = TimeDiscretizer([6,14,22])

print d.intervals

print time.ctime(1410654700)
print d.discretize(1410654700)
