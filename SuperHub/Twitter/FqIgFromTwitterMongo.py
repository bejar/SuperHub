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



def transform_fqr(tdata):
    if tdata[8] == ' ' or tdata[9] == ' ':
        return None
    else:
        return {
                  'fqurl': tdata[1],
                  'fqtime': tdata[2],
                  'fqid': tdata[4],
                  'gender': tdata[5].replace('\"','').replace('{','').replace('[','').replace(']','').replace('}',''),
                  'venueid': tdata[6],
                  'venuename': tdata[7],
                  'venuelat': float(tdata[8]),
                  'venuelng': float(tdata[9]),
                  'venuecat': tdata[10],
                  'venuepluralname': tdata[11],
                  'venueshortname': tdata[12],
                  'venueurl': tdata[13]
              }



def transform_igr(tdata):
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


def find_first_second_fq(val,list):
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


def find_first_fq(val,list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if val == list[pos][0]:
            found= True
        else:
            pos += 1
    if not found:
        return find_first_second_fq(val,list)
    else:
        return list[pos][-1]

def find_first_ig(val, list):
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



def hack_val_fq(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"','').replace('{','').replace('[','')
        vals.append( vr.split(':'))
    #print vals
    return vals


def hack_val_ig(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"','')
        vals.append( vr.split(':'))
    return vals


def extract_vals(vals, patt):
    res = []
    for p in patt:
        #print p
        val = find_first_fq(p,vals)
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
                res.extend(extract_vals(hack_val_fq(chk),chkinvals_fq))
                user = z[puser+7:pvenue-2]
                user = user.replace('}','')
                res.extend(extract_vals(fix_bval(['user', '{id'], 'id', hack_val_fq(user)), uservals_fq))
                venue = z[pvenue+9:pfvenue-1].replace('{\"id\"', 'id')
                venue = venue.replace('}', '')
                #print venue
                res.extend(extract_vals(hack_val_fq(venue), venuevals_fq))
        return res
    else:
        return None


def chop_ig(url):
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
                res.extend(extract_vals(hack_val_ig(chk),uservals_ig))
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
        if lasttwid < t['twid']:
            lasttwid = t['twid']
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
                            #print 'VALS:', vals
                            if len(vals) == 14:
                                upd = transform_fqr(vals)
                                if upd is not None:
                                    col.update({'twid': vals[0]}, {'$set': {"foursquare": upd}})
                                    print 'TWID FQ:', vals[0]
                        else: # If not successful go to next
                            print 'Unsuccessfully'
                        cnt += 1

                    elif 'http://instagram' in resp.url:
                        print cnt, time.ctime(int(t['time']),)
                        print t['tweet']
                        #print resp.url
                        cnt += 1
                        vals = [str(t['twid']), str(t['lat']), str(t['lng']), resp.url.rstrip()]
                        url = vals[3]
                        val = chop_ig(url)
                        if val is None: # Try a second time
                            time.sleep(2)
                            val = chop_ig(url)
                            #print 'Trying a second time ...'
                        if val is not None:
                            vals.extend(val)
                            #print vals
                            upd = transform_igr(vals)
                            if upd is not None:
                                col.update({'twid': vals[0]}, {'$set': {"instagram": upd}})
                                print 'TWID IG:', vals[0]

                    if cnt % 100 == 0:
                        time.sleep(5)
                        print 'Sleeping ...'


                except ValueError as e:
                    print 'ValueError:', e
                except IOError as e:
                    print 'IOError', e, url
                except UnicodeError as e:
                    print 'UnicodeError', e
                except urllib2.httplib.BadStatusLine:
                    pass
                except urllib2.HTTPError:
                    print 'HTTPError'

    col = db['Params']
    col.update({'update': 'foursquare'}, {'$set': {"ltwid": lasttwid}})

chkinvals_fq = ['createdAt', 'type']
uservals_fq = ['id','gender']
venuevals_fq = ['id', 'name', 'lat', 'lng', 'categories', 'pluralName', 'shortName', 'canonicalUrl']

uservals_ig = ['id','username']


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

