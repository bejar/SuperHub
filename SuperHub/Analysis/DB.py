# -*- coding: utf-8 -*-
"""
.. module:: DB

DB
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
import subprocess
import shutil

from pymongo import MongoClient
import pymysql
from pymysql.err import MySQLError

from Parameters.Constants import homepath
from Parameters.Private import mgpass, mguser
from Parameters.Pconstants import msqldb, msqldbs, msqlpass, msqluser


def getApplicationData2(cityparam):
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]
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


def getApplicationDataInterval(cityparam, application, intinit, intend=None):
    """Get the data events from the database and saves it in a csv file

    :param: application
    :param: cpath
    :param: square
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]
    cityname = cityparam[2]
    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    if intend is None:
        intend = int(time.time())
    print intend


    #    names= db.collection_names()
    print 'Retrieving Data ...'
    rfile = open(homepath + 'Data/' + cityname + '-' + application + '-' + str(intinit) + '.csv', 'w')
    #    rfile.write('#lat; lng; time; user\n')
    rfile.write('#lat; lng; time; user; geohash\n')
    rfile.flush()
    col = db['sndata']
    # c = col.find({'app': application,
    #               'lat': {'$gt': minLat, '$lt': maxLat},
    #               'lng': {'$gt': minLon, '$lt': maxLon},
    #              }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})

    c = col.find({'app': application,
                      'lat': {'$gt': minLat, '$lt': maxLat},
                      'lng': {'$gt': minLon, '$lt': maxLon},
                      'interval': {'$gt': intinit, '$lt': intend}
                     }, {'text': 1, 'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1}, timeout=False)

    #c = col.find({'app': application}, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})

    #subprocess.call('rm ' + homepath + 'Data/' + application + '.csv.bz2')
    print 'Saving Data ...'
    for t in c:
        #        stime=time.localtime(t['interval'])
        #        evtime=time.strftime('%Y%m%d',stime)
        #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
        #  rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])
        # +',\''+str(t['text']).strip().replace('\n','')+'\'\n')
        if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon) and (intinit < t['interval'] < intend):
            rfile.write(str(t['lat']) + ';' + str(t['lng']) + ';'
                        + str(t['interval']) + ';' + str(t['user'])
                        + ';' + t['geohash'] + '\n')
            rfile.flush()
    rfile.close()
    #subprocess.call('bzip2 ' + homepath + 'Data/' + application + '.csv')
    print 'Done'


def getApplicationData(cityparam, application):
    """Get the data events from the database and saves it in a csv file

    :param: application
    :param: cpath
    :param: square
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]
    cityname = cityparam[2]
    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    #    names= db.collection_names()
    print 'Retrieving Data ...'
    rfile = open(homepath + 'Data/' + cityname +'-'+ application  + '.csv', 'w')
    #    rfile.write('#lat; lng; time; user\n')
    rfile.write('#lat; lng; time; user; geohash\n')
    col = db['sndata']
    # c = col.find({'app': application,
    #               'lat': {'$gt': minLat, '$lt': maxLat},
    #               'lng': {'$gt': minLon, '$lt': maxLon},
    #              }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
    c = col.find({'app': application}, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})

    #subprocess.call('rm ' + homepath + 'Data/' + application + '.csv.bz2')
    print 'Saving Data ...'
    for t in c:
        #        stime=time.localtime(t['interval'])
        #        evtime=time.strftime('%Y%m%d',stime)
        #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
        #  rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])
        # +',\''+str(t['text']).strip().replace('\n','')+'\'\n')
        if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
            rfile.write(str(t['lat']) + ';' + str(t['lng']) + ';'
                        + str(t['interval']) + ';' + str(t['user'])
                        + ';' + t['geohash'] + '\n')
            rfile.flush()
    rfile.close()
    #subprocess.call('bzip2 ' + homepath + 'Data/' + application + '.csv')
    print 'Done'


def getLApplicationData(cityparam, lapplication):
    """
    Retrieves data from a lists of Social applications
    Saves an individual file for each application
    and a file with all the data

    :param lapplication:
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]

    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    #    names= db.collection_names()
    appname = ''
    apfiles = []
    apnames = []
    for ap in lapplication:
        apfile = open(homepath + 'Data/' + ap + '.csv', 'w')
        apfile.write('#lat; lng; time; user\n')
        apfiles.append(apfile)
        appname = appname + ap
        apnames.append(homepath + 'Data/' + ap + '.csv')
        shutil.move(homepath + 'Data/' + ap + '.csv.bz2', homepath + 'Data/' + ap + '.csv.old.bz2')
    shutil.move(homepath + 'Data/' + appname + '.csv.bz2', homepath + 'Data/' + appname + '.csv.old.bz2')
    rfile = open(homepath + appname + 'Data/' + '.csv', 'w')
    #    rfile.write('#lat; lng; time; user\n')
    rfile.write('#lat; lng; time; user\n')

    col = db['sndata']

    for application, apfile in zip(lapplication, apfiles):
        print 'Retrieving Data ...', application
        c = col.find({'app': application,
                      'lat': {'$gt': minLat, '$lt': maxLat},
                      'lng': {'$gt': minLon, '$lt': maxLon}}
                     , {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
        apfile.write('#lat; lng; time; user\n')
        print 'Saving Data ...', application
        for t in c:
            #stime=time.localtime(t['interval'])
            #evtime=time.strftime('%Y%m%d',stime)
            #        vtime=time.strftime('%Y%m%d%H%M%w',stime)
            #rfile.write(str(t['lat'])+','+str(t['lng'])+','+vtime+','+str(t['user'])
            # +',\''+str(t['text']).strip().replace('\n','')+'\'\n')
            if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
                rfile.write(str(t['lat']) + ';' + str(t['lng']) + ';' + str(t['interval']) + ';' + str(
                    t['user']) + '\n')  #+';'+t['geohash']+'\n')
                apfile.write(str(t['lat']) + ';' + str(t['lng']) + ';' + str(t['interval']) + ';' + str(
                    t['user']) + '\n')  #+';'+t['geohash']+'\n')
    rfile.close()
    subprocess.call(['bzip2 '], [homepath + 'Data/' + application + '.csv'])

    for f, n in zip(apfiles, apnames):
        f.close()
        subprocess.call(['bzip2 '], [n])
    print 'Done'


def transferApplicationData(cityparam, application):
    """
    Trasfers data from

    :param: application:
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]

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


def getApplicationDataOne(cityparam, application):
    """

    :param: application:
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]

    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)


    #    names= db.collection_names()
    col = db['sndata']
    # c = col.find_one({'app': application,
    #                   'lat': {'$gt': minLat, '$lt': maxLat},
    #                   'lng': {'$gt': minLon, '$lt': maxLon},
    #                  }, {'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1})
    c = col.find_one({'app': application})
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(c)


def getTweets(cityparam, intinit=None):
    """
    Gets tweets texts from the database

    :param: application:
    """
    mgdb = cityparam[0]
    minLat, maxLat, minLon, maxLon = cityparam[1]

    client = MongoClient(mgdb)

    db = client.superhub

    db.authenticate(mguser, password=mgpass)

    intend = int(time.time())
    print intend

    #    names= db.collection_names()
    col = db['sndata']
    c = col.find({'app': 'twitter',
                 'lat': {'$gt': minLat, '$lt': maxLat},
                 'lng': {'$gt': minLon, '$lt': maxLon},
                 'interval': {'$gt': intinit, '$lt': intend}
                  }, {'text': 1, 'lat': 1, 'lng': 1, 'interval': 1, 'user': 1, 'geohash': 1}, timeout=False)
    return c

