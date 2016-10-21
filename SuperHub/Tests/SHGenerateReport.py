"""
.. module:: SHGenerateReport

SHGenerateReport
*************

:Description: SHGenerateReport

    

:Authors: bejar
    

:Version: 

:Created on: 13/06/2014 10:13 

"""

__author__ = 'bejar'

from Parameters.Constants import homepath, cityparams
from Analysis.STData import STData
from Analysis.Descriptive import data_histograms
import time

dates = ['01092015', '01092016']
for net in ['twitter']:
    for city in ['bcn', 'london', 'paris', 'milan', 'rome', 'berlin']:
        data = STData(homepath, cityparams[city], net)
        data.read_DB_time(str(int(time.mktime(time.strptime(dates[0],'%d%m%Y')))), str(int(time.mktime(time.strptime(dates[1],'%d%m%Y')))))
        #data.read_DB()
        data.info()

        data_histograms(data, lhh=[(20, 200000)], dates=dates)


#data.select_heavy_hitters(100, 20000)
# transactions = DailyTransactions(data)
# fr = transactions.users_daily_length()
#
#
# today = time.strftime('%Y%m%d%H%M%S', time.localtime())
# homepathr = homepath + 'Results/'
# nfile = '-nusr' + str(100) + '#' + str(20000) + '-ts' + today
# application = data.application
#
# np.savetxt(homepathr + application + '-length' + nfile + '.csv', fr, fmt='%d')

### Do things with the data

#plot_accumulated_events(data,distrib=False,scale=300)
#accumulatedEvents('twitter',5,3000,distrib=False,scale=200)
#event_histograms('bcn-instagram-1380578300',5,5000)
#daily_histogram('twitterinstagram',5,5000)
#hourly_histogram('twitterinstagram',5,5000)
#pp = pprint.PrettyPrinter(indent=4)

#data_histograms('instagram',lhh=[(0, 20000)])
#data_histograms('twitter',lhh=[(0,20000)])
#getApplicationData('twitter')
#hourly_histogram('instagram',5,4000)

#saveDailyTransactions('hh','twitter',5,8000,scale=200)

#transferApplicationData('twitter')


#transaction_routes_many(data,lhh=[(100, 20000)], lscale=[100,200], supp=30, ltimeres=[4])

#user_events_histogram('twitter',100,20000,300,4)
#user_events_histogram('bcn-instagram-1380578300', [100,20000], 300, 4)

#montly_histogram('twitter', 0, 20000)

#user_events_histogram(data)