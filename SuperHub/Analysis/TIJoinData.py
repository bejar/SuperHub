"""
.. module:: TIJoinData

TIJoinData
*************

:Description: TIJoinData

    

:Authors: bejar
    

:Version: 

:Created on: 02/04/2014 8:30 

"""

__author__ = 'bejar'

from numpy import loadtxt


class TIJoinData:
    """
    Class for the Twitter Instagram Data

    Process the twitter data that refers to instagram posts

    Stores the twitter users id and their instagram id
    """
    wpath = None
    application = None
    dataset = None
    correspondence = {}

    def __init__(self, path, application):
        self.wpath = path
        self.application = application


    def read_data(self):
        """
        Loads the data from the csv file

        """
        print 'Reading Data ...'
        fname = self.wpath + 'Data/' + self.application + '.csv'
        self.dataset = loadtxt(fname, skiprows=1,
                               dtype=[('lat', 'f8'), ('lng', 'f8'), ('time', 'i32'), ('twuser', 'S20'),
                                      ('iguser', 'S20')],
                               usecols=(0, 1, 2, 3, 6), delimiter=';', comments='#')

    def generate_correspondences(self):
        """
        Generates a datastructure (dictionary) of the correspondences
        between  twitter id and instagram id
        @return:
        """
        for i in range(self.dataset.shape[0]):
            if not self.dataset[i][3].strip() in self.correspondence:
                self.correspondence[self.dataset[i][3].strip()] = self.dataset[i][4].strip()




