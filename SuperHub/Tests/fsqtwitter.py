# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 14:17:20 2014

@author: bejar
"""

import urllib2
import time

from bs4 import BeautifulSoup

from src.Parameters.Constants import homepath


def fix_bval(bval, gval, lval):
    rval = []
    for v in lval:
        if v[0] == bval[0] and v[1] == bval[1]:
            res = [gval, v[-1]]
        else:
            res = v
        rval.append(res)
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
    print vals
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
        time.sleep(60)
        error = True

    if not error:
        soup = BeautifulSoup(data)
        res=[]
        for link in soup.find_all('script'):
            z = link.get_text()
            if 'Checkin' in z:
                pchk = z.find('checkin:')
                puser = z.find('user')
                pvenue = z.find('venue')
                pfvenue = z.find('fullVenue')
                chk = z[pchk+11:puser-2]
                res.extend(extract_vals(hack_val(chk),chkinvals))
                user = z[puser+7:pvenue-2]
                res.extend(extract_vals(fix_bval(['user', '{id'], 'id',hack_val(user)),uservals))
                print z[pvenue+7:pfvenue-1]
                venue = z[pvenue+7:pfvenue-1].replace('{\"id\"','id')
                res.extend(extract_vals(fix_bval(['location', '{lat'], 'lat', hack_val(venue)), venuevals))
        return res
    else:
        return None

uservals = ['id','gender']
chkinvals = ['createdAt', 'type']
venuevals = ['id', 'name', 'lat', 'lng', 'categories', 'pluralName', 'shortName', 'canonicalUrl']

for nfile in ['']:
    rfile = open(homepath + nfile + '.csv', 'r')
    wfile = open(homepath + nfile + '.pr.csv', 'w')
    wfile.write('#lat; lng; time; user; geohash, url; fsqtime; fsqact; fsqusr; gender; placeid; place; fsqlat; fsqlng;'
                'vntypeid; vntname; vntshtname; fsqurl\n')

    r = rfile.readline()
    cnt = 0
    for lines in rfile:
        vals = lines.split(';')
        url = vals[5]
        val = chop_fsq(url)
        if val is None: # Try a second time
            val = chop_fsq(url)
            print 'Trying a second time ...'
        if val is not None:
            time.sleep(5)
            vals.extend(val)
            print vals
            i = 0
            for v in vals:
                wfile.write(v.encode('ascii', 'ignore').rstrip())
                i += 1
                if i < len(vals):
                    wfile.write('; ')

            wfile.write('\n')
            wfile.flush()
        else: # If not successful go to next
            print 'Unsuccessfully'
        cnt +=1
        if cnt % 100 == 0:
            time.sleep(180)
            print 'Sleeping ...'



