"""
.. module:: instatwitter

instatwitter
*************

:Description: instatwitter

    

:Authors: bejar
    

:Version: 

:Created on: 12/03/2014 8:33 

"""

__author__ = 'bejar'

import urllib2
import time

from bs4 import BeautifulSoup
from pymongo import MongoClient

from Parameters.Pconstants import mglocal


def transform(tdata):
   return {
        'lat': tdata[1],
        'lng': tdata[2],
        'igurl': tdata[3],
        'igid': tdata[4],
        'iguname': str(tdata[5])
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


def find_first(val, list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if val == list[pos][0]:
            found= True
        else:
            pos += 1
    if not found:
        return None
    else:
        return list[pos][-1]

def hack_val(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"','')
        vals.append( vr.split(':'))
    return vals

def extract_vals(vals, patt):
    res = []
    for p in patt:
        val = find_first(p,vals)
        if val is not None:
            res.append(val)
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
            if '_sharedData' in z:
                powner = z.find('owner')
                pfowner = z.find(',\"__get_params')
                chk = z[powner+8:pfowner-2]
                res.extend(extract_vals(hack_val(chk),uservals))
        return res
    else:
        return None

def do_the_job(ltwid):
    mgdb = mglocal[0]
    client = MongoClient(mgdb)
    db = client.local
    db.authenticate(mglocal[2], password=mglocal[3])
    col = db[mglocal[1]]

    cursor = col.find({'twid': {'$gt': ltwid}}, {'tweet': 1, 'twid': 1, 'time': 1, 'lat': 1, 'lng': 1}, timeout=False)

    cnt = 0
    lasttwid = ''
    for t in cursor:
        if 'I\'m at' in t['tweet'] or 'http' in t['tweet']:
            text = t['tweet'].split()
            url = None
            for p in text:
                if 'http' in p:
                    url = p[p.find('http'), :]
                    if '\"' in url:
                        url = url[0, url.find('\"')]
            if url is not None:
                try:
                    resp = urllib2.urlopen(url.encode('ascii', 'ignore'), timeout=5)
                    if 'http://instagram' in resp.url:
                        print cnt, time.ctime(int(t['time']),)
                        print t['tweet']
                        #print resp.url
                        cnt += 1
                        vals = [str(t['twid']), str(t['lat']), str(t['lng']), resp.url.rstrip()]
                        url = vals[3]
                        val = chop_fsq(url)
                        if val is None: # Try a second time
                            time.sleep(2)
                            val = chop_fsq(url)
                            #print 'Trying a second time ...'
                        if val is not None:
                            vals.extend(val)
                            print vals
                            upd = transform(vals)
                            if upd is not None:
                                col.update({'twid': vals[0]}, {'$set': {"instagram": upd}})
                                print 'TWID:', vals[0]

                        if cnt % 100 == 0:
                            time.sleep(5)


                except IOError as e:
                    print 'IO Error', e
                except UnicodeError as e:
                    print 'Unicode Error', e
                except ValueError as e:
                    print 'Value Error', e
                except urllib2.httplib.BadStatusLine:
                    pass
    col = db['Params']
    col.update({'update': 'instagram'}, {'$set': {"ltwid": lasttwid}})


uservals = ['id','username']

mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db['Params']

cursor = col.find({'update': 'instagram'}, {'ltwid': 1}, timeout=False)
ltw = None
for t in cursor:
    ltw = t['ltwid']

print ltw



do_the_job(ltw)

