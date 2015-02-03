"""
.. module:: ClusterCompare

ClusterCompare
*************

:Description: ClusterCompare

    

:Authors: bejar
    

:Version: 

:Created on: 31/10/2014 10:20 

"""

__author__ = 'bejar'

from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, normalized_mutual_info_score
from numpy import loadtxt

def compute_sim(clfiles):
    lclust = []

    for c in clfiles:
        data = loadtxt(homepath + c + '.csv',
                       dtype=[('cluster', 'S20'), ('user', 'S20')],
                       usecols=(0, 1), delimiter=',', comments='#')
        data.sort(order='user')
        ex = [data[i][0] for i in range(data.shape[0])]
        lclust.append(ex)

    print 'NMI= '
    for i in range(len(lclust)-1):
        for j in range(i+1, len(lclust)):
            print normalized_mutual_info_score(lclust[i], lclust[j]),
        print
    print
    print 'ARAND= '
    for i in range(len(lclust)-1):
        for j in range(i+1, len(lclust)):
            print adjusted_rand_score(lclust[i], lclust[j]),
        print
    print
    print 'AMI= '
    for i in range(len(lclust)-1):
        for j in range(i+1, len(lclust)):
            print adjusted_mutual_info_score(lclust[i], lclust[j]),
        print
    print



homepath = '/home/bejar/Documentos/Investigacion/Papers/SuperHubClustering/data/'

# clfiles = ['bcntwitter-septemberbin-labels-kmeans-minloc20-minsize0-timed[6, 18]-nclust60-nusr50#70000-r0.0025',
#            'bcntwitter-septemberbin-labels-affinity-minloc20-minsize0-timed[6, 18]-damp0.5-nusr50#70000-r0.0025',
#            'bcntwitter-septemberbin-labels-spectral-minloc20-minsize0-timed[6, 18]-nclust60-nusr50#70000-r0.0025'
#            ]


#for dtime in ['[6, 18]','[6, 16, 22]','[6, 16, 18, 22]']:
for dtime in ['[6, 18]']:
    for disc in [ '0.005']:
        lfiles = []

        lfiles.append('bcntwitter-septemberbin-labels-affinity-minloc20-minsize20-timed%s-damp0.5-nusr50#70000-r%s' % (dtime, disc))
        #lfiles.append('bcntwitter-septemberbin-labels-affinity-minloc20-minsize20-timed%s-damp0.75-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-affinity-minloc20-minsize20-timed%s-damp0.999-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-kmeans-minloc20-minsize20-timed%s-nclust60-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-kmeans-minloc20-minsize20-timed%s-nclust80-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-kmeans-minloc20-minsize20-timed%s-nclust100-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-spectral-minloc20-minsize20-timed%s-nclust60-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-spectral-minloc20-minsize20-timed%s-nclust80-nusr50#70000-r%s' % (dtime, disc))
        lfiles.append('bcntwitter-septemberbin-labels-spectral-minloc20-minsize20-timed%s-nclust100-nusr50#70000-r%s' % (dtime, disc))
        print '-------------\n',dtime, disc
        compute_sim(lfiles)
















