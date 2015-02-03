"""
.. module:: fsqtwitter2

fsqtwitter2
*************

:Description: fsqtwitter2

    

:Authors: bejar
    

:Version: 

:Created on: 12/03/2014 7:47 

"""

__author__ = 'bejar'

import urllib2
import time

from bs4 import BeautifulSoup
from pymongo import MongoClient

from Parameters.Pconstants import mglocal


def transform(tdata):
    if tdata[8] == ' ' or tdata[7] == ' ':
        return None
    else:
        return {
                  'fqurl': tdata[1],
                  'fqtime': tdata[2],
                  'fqid': tdata[3],
                  'gender': tdata[4].replace('\"','').replace('{','').replace('[','').replace(']','').replace('}',''),
                  'venueid': tdata[5],
                  'venuename': tdata[6],
                  'venuelat': float(tdata[7]),
                  'venuelng': float(tdata[8]),
                  'venuecat': tdata[9],
                  'venuepluralname': tdata[10],
                  'venueshortname': tdata[11],
                  'venueurl': tdata[12]
              }

def fix_bval(bval, gval, lval):
    rval = []
    for v in lval:
        if v[0] == bval[0] and v[1] == bval[1]:
            r = [gval, v[-1]]
        else:
            r = v
        rval.append(r)
    return rval


def find_first_second(val,list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if len(list[pos]) > 1 and val == list[pos][1]:
            found= True
        else:
            pos += 1
    if not found:
        return None
    else:
        if len(list[pos]) > 2:
            return list[pos][-1]
        else:
            return None


def find_first(val,list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if val == list[pos][0]:
            found= True
        else:
            pos += 1
    if not found:
        return find_first_second(val,list)
    else:
        return list[pos][-1]

def hack_val(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"','').replace('{','').replace('[','')
        vals.append( vr.split(':'))
    #print vals
    return vals

def extract_vals(vals, patt):
    res = []
    for p in patt:
        #print p
        val = find_first(p,vals)
        if val is not None:
            res.append(val)
            #print val
        else:
            res.append('')
    return res


def chop_fsq(url):
    error = False
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
    except urllib2.HTTPError:
        time.sleep(15)
        error = True

    if not error:
        soup = BeautifulSoup(data)
        res=[]
        for link in soup.find_all('script'):
            z = link.get_text()
            if 'Checkin' in z:
                pchk = z.find('checkin:')
                puser = z.find('user')
                pvenue = z.find('venue\"')
                pfvenue = z.find('fullVenue')
                chk = z[pchk+11:puser-2]
                res.extend(extract_vals(hack_val(chk),chkinvals))
                user = z[puser+7:pvenue-2]
                user = user.replace('}','')
                res.extend(extract_vals(fix_bval(['user', '{id'], 'id', hack_val(user)), uservals))
                venue = z[pvenue+9:pfvenue-1].replace('{\"id\"', 'id')
                venue = venue.replace('}', '')
                #print venue
                res.extend(extract_vals(hack_val(venue), venuevals))
        return res
    else:
        return None


def do_the_job(ltwid):

    mgdb = mglocal[0]
    client = MongoClient(mgdb)
    db = client.local
    db.authenticate(mglocal[2], password=mglocal[3])
    col = db[mglocal[1]]

    cursor = col.find({'twid': {'$gt': ltwid}}, {'tweet': 1, 'twid': 1, 'time': 1}, timeout=False)
    cnt = 0
    lasttwid = ''
    for t in cursor:
        if 'I\'m at' in t['tweet'] or 'http' in t['tweet']:
            if lasttwid < t['twid']:
                lasttwid = t['twid']
            text = t['tweet'].split()
            url = None
            for p in text:
                if 'http' in p:
                    url = p
            if url is not None:
                try:
                    resp = urllib2.urlopen(url, timeout=5)
                    if 'foursquare' in resp.url or 'swarmapp' in resp.url:
                        print cnt, time.ctime(int(t['time'])),
                        print t['tweet']
                        print resp.url
                        vals = [str(t['twid']), resp.url.rstrip()]
                        url = vals[1]
                        val = chop_fsq(url)
                        if val is None: # Try a second time
                            time.sleep(2)
                            val = chop_fsq(url)
                            print 'Trying a second time ...'
                        if val is not None:
                            vals.extend(val)
                            print '*****************', vals
                            upd = transform(vals)
                            print upd
                            if upd is not None:
                                print vals[0]
                                col.update({'twid': vals[0]}, {'$set': {"foursquare": upd}})
                                print 'TWID:', vals[0]
                        else: # If not successful go to next
                            print 'Unsuccessfully'
                        cnt += 1
                        if cnt % 100 == 0:
                            time.sleep(5)
                            print 'Sleeping ...'


                except ValueError:
                    pass
                except IOError:
                    pass
                except UnicodeError:
                    pass
                except urllib2.httplib.BadStatusLine:
                    pass
    col = db['Params']
    col.update({'update': 'foursquare'}, {'$set': {"ltwid": lasttwid}})

chkinvals = ['createdAt', 'type']
uservals = ['id','gender']
venuevals = ['id', 'name', 'lat', 'lng', 'categories', 'pluralName', 'shortName', 'canonicalUrl']

mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db['Params']

cursor = col.find({'update': 'foursquare'}, {'ltwid': 1}, timeout=False)
ltw = None
for t in cursor:
    ltw = t['ltwid']

print ltw

do_the_job(ltw)

