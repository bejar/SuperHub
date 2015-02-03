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

from src.Parameters.Constants import homepath, bcnparam
from Analysis.DB import getTweets


def fix_bval(bval, gval, lval):
    rval = []
    for v in lval:
        if v[0] == bval[0] and v[1] == bval[1]:
            r = [gval, v[-1]]
        else:
            r = v
        rval.append(r)
    return rval


def find_first(val,list):
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

uservals = ['id','username']

city = bcnparam[2]
minLat, maxLat, minLon, maxLon = bcnparam[1]

#rfile = open(homepath + 'twitter+fsq-12.csv', 'r')
wfile = open(homepath + city + '-twitter+instagram-1415603700.pr.csv', 'w')
#wfile.write('#lat; lng; time; user; geohash; url; instaid; instauser\n')


tw = getTweets(bcnparam, intinit=1415603700)

cnt = 0
for t in tw:
    if 'I\'m at' in t['text'] or 'http' in t['text']:
        text = t['text'].split()
        url = None
        for p in text:
            if 'http' in p:
                url = p
        if url is not None:
            try:
                resp = urllib2.urlopen(url,timeout=5)
                if 'http://instagram' in resp.url:

                    if (minLat <= t['lat'] < maxLat) and (minLon <= t['lng'] < maxLon):
                        print cnt, time.ctime(t['interval']),
                        print t['text']
                        #print resp.url
                        cnt += 1
                        vals = [str(t['lat']), str(t['lng']), str(t['interval']), str(t['user']), t['geohash'],
                                resp.url.rstrip()]
                        url = vals[5]
                        val = chop_fsq(url)
                        if val is None: # Try a second time
                            val = chop_fsq(url)
                            #print 'Trying a second time ...'
                        if val is not None:
                            time.sleep(2)
                            vals.extend(val)
                            #print vals
                            i = 0
                            for v in vals:
                                wfile.write(v.encode('ascii', 'ignore').rstrip())
                                i += 1
                                if i < len(vals):
                                    wfile.write('; ')

                            wfile.write('\n')
                            wfile.flush()
                        #else: # If not successful go to next
                            #print 'Unsuccessfully'
                        if cnt % 100 == 0:
                            time.sleep(20)
                            #print 'Sleeping ...'



            except IOError:
                pass
            except UnicodeError:
                pass
            except ValueError:
                pass
            except urllib2.httplib.BadStatusLine:
                pass

