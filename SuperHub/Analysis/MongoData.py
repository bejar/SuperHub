"""
.. module:: MongoData

MongoData
*************

:Description: MongoData

    

:Authors: bejar
    

:Version: 

:Created on: 09/02/2015 9:28 

"""

__author__ = 'bejar'

class MongoData:
    def __init__(self, db, user, passwd, collect):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.collection= collect

