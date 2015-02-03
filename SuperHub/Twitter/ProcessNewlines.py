"""
.. module:: ProcessNewlines

ProcessNewlines
*************

:Description: ProcessNewlines

    

:Authors: bejar
    

:Version: 

:Created on: 02/12/2014 10:28 

"""

__author__ = 'bejar'

import os

from src.Parameters.Constants import homepath

for nfile in os.listdir(homepath+'Data-py/'):

    print nfile
    if 'csv' in nfile:
        rfile = open(homepath+'Data-py/'+ nfile, 'r')
        wfile = open(homepath + 'Data-py/' + nfile.replace('.csv', '.proc.csv'), 'w')


        ln = ''
        for lines in rfile:
            if lines[-5:-1] == '###)':
                ln += lines
                wfile.write(ln.replace('\n', ' ').replace('\r', '')+'\n')
                ln = ''
            else:
                ln += lines

