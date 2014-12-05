"""
.. module:: Data

Data
*************

:Description: Data

    

:Authors: bejar
    

:Version: 

:Created on: 05/12/2014 12:35 

"""

__author__ = 'bejar'



parts = ['twid', 'username', 'user', 'lng', 'lat', 'interval', 'text']

def getTweetsParts(line):
    res = {}
    st = 0
    for i in range(len(parts)-1):
        pos = line.find(';', st)
        res[parts[i]] = line[st:pos-1]
        st = pos + 1
    res[parts[-1]] = line[st:-1]
    return res