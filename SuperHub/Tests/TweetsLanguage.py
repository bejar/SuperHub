# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:14:45 2013

@author: bejar
"""

from pymongo import MongoClient
from guess_language import guessLanguageInfo

cpath = '/home/bejar/Documentos/Investigacion/SuperHub/tweetdata/'


def getLanguage():
    client = MongoClient('mongodb://atalaya-barcelona.mooo.com:27017/')

    db = client.superhub

    db.authenticate('superhubadmin', password='1988glmek')

    col = db['sndata']
    c = col.find({'app': 'twitter'})
    for i in range(100):
        text = str(c[i]['text']).strip().replace('\n', '')
        lang = guessLanguageInfo(text)
        print text
        print lang


getLanguage()


