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
import logging

from bs4 import BeautifulSoup
from pymongo import MongoClient

from Parameters.Pconstants import mglocal


def transform_fqr(tdata):
    if tdata[8] == ' ' or tdata[9] == ' ':
        return None
    else:
        return {'fqurl': tdata[1],
                'fqtime': tdata[2],
                'fqid': tdata[4],
                'gender': tdata[5].replace('\"', '').replace('{', '').replace('[', '').replace(']', '').replace('}',
                                                                                                                ''),
                'venueid': tdata[6],
                'venuename': tdata[7].strip(),
                'venuelat': float(tdata[8]),
                'venuelng': float(tdata[9]),
                'venuecat': tdata[10].strip(),
                'venuepluralname': tdata[11].strip(),
                'venueshortname': tdata[12].strip(),
                'venueurl': tdata[13]
                }


def transform_igr(tdata):
    if len(tdata) < 6:
        return None
    else:
        res = {'lat': tdata[1],
               'lng': tdata[2],
               'igurl': tdata[3],
               'igid': tdata[4],
               'iguname': str(tdata[5]).strip()}
        if len(tdata) > 6:
            res['iglocid'] = tdata[6].strip()
        if len(tdata) > 7:
            res['iglocname'] = tdata[7].strip()

        return res


def fix_bval(bval, gval, lval):
    rval = []
    for v in lval:
        if v[0] == bval[0] and v[1] == bval[1]:
            r = [gval, v[-1]]
        else:
            r = v
        rval.append(r)
    return rval


def find_first_second_fq(val, list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if len(list[pos]) > 1 and val == list[pos][1]:
            found = True
        else:
            pos += 1
    if not found:
        return None
    else:
        if len(list[pos]) > 2:
            return list[pos][-1]
        else:
            return None


def find_first_fq(val, list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if val == list[pos][0]:
            found = True
        else:
            pos += 1
    if not found:
        return find_first_second_fq(val, list)
    else:
        return list[pos][-1]


def find_first_ig(val, list):
    found = False
    pos = 0
    while not found and pos < (len(list)):
        if val == list[pos][0]:
            found = True
        else:
            pos += 1
    if not found:
        return None
    else:
        return list[pos][-1]


def hack_val_fq(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"', '').replace('{', '').replace('[', '')
        vals.append(vr.split(':'))
    # print vals
    return vals


def hack_val_ig(val):
    vals = []
    for v in val.split(','):
        vr = v.replace('\"', '')
        vals.append(vr.split(':'))
    return vals


def extract_vals(vals, patt):
    res = []
    for p in patt:
        # print p
        val = find_first_fq(p, vals)
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
        res = []
        for link in soup.find_all('script'):
            z = link.get_text()
            if 'Checkin' in z:
                pchk = z.find('checkin:')
                puser = z.find('user')
                pvenue = z.find('venue\"')
                pfvenue = z.find('fullVenue')
                chk = z[pchk + 11:puser - 2]
                res.extend(extract_vals(hack_val_fq(chk), chkinvals_fq))
                user = z[puser + 7:pvenue - 2]
                user = user.replace('}', '')
                res.extend(extract_vals(fix_bval(['user', '{id'], 'id', hack_val_fq(user)), uservals_fq))
                venue = z[pvenue + 9:pfvenue - 1].replace('{\"id\"', 'id')
                venue = venue.replace('}', '')
                # print venue
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
        res = []
        for link in soup.find_all('script'):
            z = link.get_text()
            if '_sharedData' in z:
                powner = z.find('owner')
                pfowner = z.find(',\"__get_params')
                chk = z[powner + 8:pfowner - 2]
                res.extend(extract_vals(hack_val_ig(chk), uservals_ig))
        return res
    else:
        return None


def do_the_job(ltwid):
    mgdb = mglocal[0]
    client = MongoClient(mgdb)
    db = client.local
    db.authenticate(mglocal[2], password=mglocal[3])
    col = db[mglocal[1]]

    cursor = col.find({'twid': {'$gt': ltwid}}, {'tweet': 1, 'twid': 1, 'time': 1, 'lat': 1, 'lng': 1})
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
                    url = p[p.find('http'):]
                    if '\"' in url:
                        url = url[0: url.find('\"')]
                        # if '\xe2' in url:
                        # url = url[0: url.find('\xe2')]
            if url is not None:
                try:
                    cnt += 1
                    resp = urllib2.urlopen(url.encode('ascii', 'ignore'), timeout=5)
                    # print resp.url
                    if 'foursquare' in resp.url or 'swarmapp' in resp.url:
                        logger.info('FQ: %d %s', cnt, time.ctime(int(t['time'])))
                        logger.info('%s', t['tweet'])
                        logger.info('%s', resp.url)
                        vals = [str(t['twid']), resp.url.rstrip()]
                        url = vals[1]
                        val = chop_fsq(url)
                        if val is None:  # Try a second time
                            time.sleep(2)
                            val = chop_fsq(url)
                            logger.info('Trying a second time ...')
                        if val is not None:
                            vals.extend(val)
                            if len(vals) == 14:
                                upd = transform_fqr(vals)
                                if upd is not None:
                                    col.update({'twid': vals[0]}, {'$set': {"foursquare": upd}})
                                    logger.info('TWID FQ: %s', vals[0])
                        else:  # If not successful go to next
                            logger.info('Unsuccessfully')

                    elif 'instagram' in resp.url:
                        logger.info('IG: %d %s', cnt, time.ctime(int(t['time']), ))
                        logger.info("%s ", t['tweet'])
                        #print resp.url
                        vals = [str(t['twid']), str(t['lat']), str(t['lng']), resp.url.rstrip()]
                        url = vals[3]
                        val = chop_ig(url)
                        if val is None:  # Try a second time
                            time.sleep(2)
                            val = chop_ig(url)
                        if val is not None:
                            vals.extend(val)
                            print vals
                            upd = transform_igr(vals)
                            if upd is not None:
                                col.update({'twid': vals[0]}, {'$set': {"instagram": upd}})
                                logger.info('TWID IG: %s', vals[0])

                                # if cnt % 100 == 0:
                                #     time.sleep(5)
                                #     logger.info('Sleeping ...')


                except ValueError as e:
                    logger.error('ValueError: %s', e)
                except IOError as e:
                    logger.error('IOError %s %s', e, url)
                except UnicodeError as e:
                    logger.error('UnicodeError %s', e)
                except urllib2.httplib.BadStatusLine:
                    pass
                except urllib2.HTTPError:
                    logger.error('HTTPError')

    col = db['Params']
    col.update({'update': 'foursquare'}, {'$set': {"ltwid": lasttwid}})

# ----------------------------------------------------------------------------------------------------

chkinvals_fq = ['createdAt', 'type']
uservals_fq = ['id', 'gender']
venuevals_fq = ['id', 'name', 'lat', 'lng', 'categories', 'pluralName', 'shortName', 'canonicalUrl']

uservals_ig = ['id', 'username', 'location', 'name']

silent = False

# Logging configuration
logger = logging.getLogger('log')
if silent:
    logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.INFO)

console = logging.StreamHandler()
if silent:
    console.setLevel(logging.ERROR)
else:
    console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('log').addHandler(console)

mgdb = mglocal[0]
client = MongoClient(mgdb)
db = client.local
db.authenticate(mglocal[2], password=mglocal[3])
col = db['Params']

cursor = col.find({'update': 'foursquare'}, {'ltwid': 1})
ltw = None
for t in cursor:
    ltw = t['ltwid']

print ltw

do_the_job(ltw)

print "The End"

