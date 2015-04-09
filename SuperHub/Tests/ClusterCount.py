"""
.. module:: ClusterCount

ClusterCount
*************

:Description: ClusterCount

    

:Authors: bejar
    

:Version: 

:Created on: 06/11/2014 8:25 

"""

__author__ = 'bejar'
from numpy import loadtxt


def count_clust(nfile, nc):
    data = loadtxt(homepath + nfile + '.csv',
                   dtype=[('cluster', 'S20'), ('count', 'd')],
                   usecols=(0, 1), delimiter=',', comments='#')
    cnt = 0
    for d in range(data.shape[0]):
        if data[d][1] > nc:
            cnt += 1
    return cnt


homepath = '/home/bejar/Documentos/Investigacion/Papers/SuperHubClustering/data/'

# clfiles = ['bcntwitter-septemberbin-labels-kmeans-minloc20-minsize0-timed[6, 18]-nclust60-nusr50#70000-r0.0025',
# 'bcntwitter-septemberbin-labels-affinity-minloc20-minsize0-timed[6, 18]-damp0.5-nusr50#70000-r0.0025',
#            'bcntwitter-septemberbin-labels-spectral-minloc20-minsize0-timed[6, 18]-nclust60-nusr50#70000-r0.0025'
#            ]


#for dtime in ['[6, 18]','[6, 16, 22]','[6, 16, 18, 22]']:
for dtime in ['[6, 18]']:
    for disc in ['0.001', '0.0025', '0.005']:
        for ncl in ['40', '60', '80', '100']:
            nfile = 'bcntwitter-septemberbin-sizes-kmeans-minloc20-minsize20-timed%s-nclust%s-nusr50#70000-r%s' % (
            dtime, ncl, disc)
            print 'Km %s %s %s %d' % (dtime, ncl, disc, count_clust(nfile, 20))
            nfile = 'bcntwitter-septemberbin-sizes-spectral-minloc20-minsize20-timed%s-nclust%s-nusr50#70000-r%s' % (
            dtime, ncl, disc)
            print 'SP %s %s %s %d' % (dtime, ncl, disc, count_clust(nfile, 20))

        for damp in ['0.5', '0.999']:
            nfile = 'bcntwitter-septemberbin-sizes-affinity-minloc20-minsize20-timed%s-damp%s-nusr50#70000-r%s' % (
            dtime, damp, disc)
            print 'Aff %s %s %s %d' % (dtime, ncl, damp, count_clust(nfile, 20))

        print '---'

