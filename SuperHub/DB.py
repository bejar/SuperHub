# -*- coding: utf-8 -*-
"""
.. module:: SuperHubData

SuperHubData
************

:Description: SuperHub data functions

    Exports data from database to csv file

    Loads data from csv file

    Performs different processings to the data matrix

:Authors:
    bejar

:Version: 1.0


"""

import time
import pprint
import operator

from pymongo import MongoClient
import pymysql
from pymysql.err import MySQLError
import numpy as np
from numpy import loadtxt

from SuperHub.Constants import minLat, maxLat, minLon, maxLon, homepath
from SuperHub.Constants import mgdb, mgpass, mguser
from SuperHub.Constants import msqldb, msqldbs, msqlpass, msqluser
import SuperHub.Data as shdata
import subprocess


def getApplicationData2():
    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    #    names= db.collection_names()
    print 'Retrieving Data ...'
    col = db['sndata']
    print col.distinct('app')
    # print  col.find({'app': application,
    #            'lat': {'$gt': minLat, '$lt': maxLat},
    #               'lng': {'$gt': minLon, '$lt': maxLon},
    #              }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1}).count()
    # print col.find({'app': application
    #              }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1}).count()
    print 'The End'


def getApplicationData(application):
    """Get the data events from the database and saves it in a csv file

    :param: application
    :param: cpath
    :param: square
    """
    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    #    names= db.collection_names()
    print 'Retrieving Data ...'
    rfile = open(homepath + application + '.csv', 'w')
    #    rfile.write('#lat; lng; time; user\n')
    rfile.write('#lat; lng; time; user\n')
    col = db['sndata']
    # c = col.find({'app': application,
    #               'lat': {'$gt': minLat, '$lt': maxLat},
    #               'lng': {'$gt': minLon, '$lt': maxLon},
    #              }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
    c = col.find({'app': application
                 }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})

    subprocess.call('rm ' + homepath + application + '.csv.bz2')
    print 'Saving Data ...'
    for t in c:
    #        stime=time.localtime(t['interval'])
    #        evtime=time.strftime('%Y%m%d',stime)
    #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
    #  rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])+',\''+str(t['text']).strip().replace('\n','')+'\'\n')
        if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
            rfile.write(str(t['lat']) + ';' + str(t['lng']) + ';'
                        + str(t['interval']) + ';' + str(t['user'])
                        + ';' + t['geohash'] + '\n')
    rfile.close()
    subprocess.call('bzip2 ' + homepath + application + '.csv')
    print 'Done'


def getLApplicationData(lapplication):
    """
    Retrieves data from a lists of Social applications
    Saves an individual file for each application
    and a file with all the data

    :param lapplication:
    """

    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)


    #    names= db.collection_names()
    appname = ''
    apfiles = []
    apnames = []
    for ap in lapplication:
        apfile = open(homepath + ap + '.csv', 'w')
        apfile.write('#lat; lng; time; user\n')
        apfiles.append(apfile)
        appname = appname + ap
        apnames.append(homepath + ap + '.csv')
        subprocess.call('rm ' + homepath + ap + '.csv.bz2')
    subprocess.call('rm ' + homepath + appname + '.csv.bz2')
    rfile = open(homepath + appname + '.csv', 'w')
    #    rfile.write('#lat; lng; time; user\n')
    rfile.write('#lat; lng; time; user\n')



    col = db['sndata']

    for application,apfile in zip(lapplication,apfiles):
        print 'Retrieving Data ...', application
        c = col.find({'app': application,
                      'lat': {'$gt': minLat, '$lt': maxLat},
                      'lng': {'$gt': minLon, '$lt': maxLon},
                     }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
        apfile.write('#lat; lng; time; user\n')
        print 'Saving Data ...', application
        for t in c:
        #stime=time.localtime(t['interval'])
        #evtime=time.strftime('%Y%m%d',stime)
        #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
        #  rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])+',\''+str(t['text']).strip().replace('\n','')+'\'\n')
            if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
                rfile.write(str(t['lat']) + ';' + str(t['lng']) + ';' + str(t['interval']) + ';' + str(
                    t['user']) + '\n')#+';'+t['geohash']+'\n')
                apfile.write(str(t['lat']) + ';' + str(t['lng']) + ';' + str(t['interval']) + ';' + str(
                    t['user']) + '\n')#+';'+t['geohash']+'\n')
    rfile.close()
    subprocess.call('bzip2 '+ homepath + application + '.csv')

    for f,n in zip(apfiles,apnames):
        f.close()
        subprocess.call('bzip2 '+ n)
    print 'Done'


def transferApplicationData(application):
    """
    Trasfers data from

    :param: application:
    """

    client = MongoClient(mgdb)
    db = client.superhub
    db.authenticate(mguser, password=mgpass)
    col = db['sndata']

    con = pymysql.connect(host=msqldb, port=3306, user=msqluser,
                          passwd=msqlpass, db=msqldbs)
    cur = con.cursor()
    timestamp = 0
    try:
        cur.execute('SELECT max(timestamp) FROM SuperHub.geodata WHERE application=%s', application)
        rows = cur.fetchall()
        timestamp = rows[0]
    except MySQLError, e:
        print "Error %d: %s" % (e.args[0], e.args[1])

    c = col.find({'app': application, 'interval': {'$gt': timestamp}})

    for t in c:
        if (minLat <= float(t['lat']) < maxLat) and (minLon <= float(t['lng']) < maxLon):
            try:
                query = "INSERT INTO geodata " \
                        "(Lat,Lon,geohash,timestamp,user,application,YMD,hour,weekday) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                stime = time.localtime(t['interval'])
                evtime = time.strftime('%Y%m%d', stime)
                cur = con.cursor()
                cur.execute(query, (float(t['lat']), float(t['lng']),
                                    t['geohash'], int(t['interval']), t['user'],
                                    application, evtime, int(stime[3]), int(stime[6])))
                con.commit()
            except MySQLError, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                con.commit()


def getApplicationDataOne(application):
    """

    :param: application:
    """
    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)


    #    names= db.collection_names()
    col = db['sndata']
    c = col.find_one({'app': application,
                  'lat': {'$gt': minLat, '$lt': maxLat},
                  'lng': {'$gt': minLon, '$lt': maxLon},
                 }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
    #c = col.find_one({'app': application})
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(c)



# def readData(application):
#     """
#     Loads the data from the csv file
#
#     :param: application:
#     :return:
#     """
#     fname = cpath + application + '.csv.bz2'
#     data = loadtxt(fname, skiprows=1, dtype=[('lat', 'f8'), ('lng', 'f8')
#         , ('time', 'i32'), ('user', 'S20')], usecols=(0, 1, 2, 3), delimiter=';', comments='#')
#     #    print data.dtype
#     return data


# def cleanDataArea(data):
#     """
#     Deletes all the events out of the interest region
#
#     :param: data:
#     :return:
#     """
#     dataclean = None
#     for i in range(data.shape[0]):
#         if (minLat <= data[i][0] < maxLat) and (minLon <= data[i][1] < maxLon):
#             if dataclean is None:
#                 aval = np.zeros((1, 4), dtype='f')
#                 aval[0, 0] = data[i][0]
#                 aval[0, 1] = data[i][1]
#                 aval[0, 2] = data[i][2]
#                 aval[0, 3] = data[i][3]
#                 dataclean = aval
#             else:
#                 aval = np.zeros((1, 4), dtype='f')
#                 aval[0, 0] = data[i][0]
#                 aval[0, 1] = data[i][1]
#                 aval[0, 2] = data[i][2]
#                 aval[0, 3] = data[i][3]
#                 dataclean = np.row_stack((dataclean, aval))
#     return dataclean


# def computeHeavyHitters(data, mxhh, mnhh):
#     """
#     Computes the list of the number of events
#     and return a list with the users between the
#     positions mxhh and mnhh in the descendent order
#
#     :param: data:
#     :param: mxhh:
#     :param: mnhh:
#     :return: list with the list of users
#     """
#     usercount = {}
#     for i in range(data.shape[0]):
#         if data[i][3] in usercount:
#             usercount[data[i][3]] += 1
#         else:
#             usercount[data[i][3]] = 1
#     sorted_x = sorted(usercount.iteritems(), key=operator.itemgetter(1), reverse=True)
#     mnhht = min(mnhh, len(sorted_x))
#     hhitters = [x for x, y in sorted_x[mxhh:mnhht]]
#     return hhitters


# def selectDataUsers(data, users):
#     """
#     Deletes all the events that are not in the user list
#
#     :param: data:
#     :param: users:
#     :return:
#     """
#     dataclean = None
#     sel = [data[i][3] in users for i in range(data.shape[0])]
#     asel = np.array(sel)
#     dataclean = data[asel]
#     return dataclean


# def hourlyTable(data):
#     """
#     Computes the accumulated events by hour for the data table
#
#     :param: data:
#     :return:
#     """
#     htable = [0 for i in range(24)]
#     for i in range(data.shape[0]):
#         stime = time.localtime(np.int32(data[i][2]))
#         evtime = stime[3]
#         htable[evtime] += 1
#     return htable
#
#
# def dailyTable(data):
#     """
#     Computes the accumulated events by day for the data table
#
#     :param: data:
#     :return:
#     """
#     htable = [0 for i in range(7)]
#     for i in range(data.shape[0]):
#         stime = time.localtime(np.int32(data[i][2]))
#         evtime = stime[6]
#         htable[evtime] += 1
#     return htable
#
#
# def monthlyTable(data):
#     """
#     Computes the accumulated events by month
#
#     @param data:
#     @return:
#     """
#     htable = [0 for i in range(12)]
#     for i in range(data.shape[0]):
#         stime = time.localtime(np.int32(data[i][2]))
#         evtime = stime[1]
#         htable[evtime - 1] += 1
#     return htable


# def heavyHittersData(application, mxhh=100, mnhh=1000):
#     """
#     Reads and deturns the data for the heavy hitters
#
#     @param application:
#     @param mxhh:
#     """
#     data = shdata(cpath,application)
#     print 'Reading Data ...'
#     data.read_data()
#     print 'Selecting Heavy Hitters ...'
#     data.select_heavy_hitters(mxhh, mnhh)
#     return data


def saveDataResult(data, fname):
    """
    Save data results in a file

    :param: data:
    :param: fname:
    """
    pass

