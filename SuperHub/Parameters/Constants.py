# -*- coding: utf-8 -*-
"""
.. module:: SuperHubConstants

Constants
************

:Description: SuperHub constants,

    The coordinates of the region of interest and the path to the data files
    And the information of the mongo database

:Authors:
    bejar

:Version: 1.0


"""

__author__ = 'bejar'

from Parameters.Pconstants import mgdbbcn, mgdbmilan, mgdbhelsinki
import numpy as np
homepath = '/home/bejar/Data/SuperHub/'

# 45.467 9.200
bcncoord = (41.20, 41.65, 1.90, 2.40)
milancoord = (45.33, 45.59, 9.03, 9.37)
hlsnkcoord = (60.02, 60.30, 24.72, 25.10)
pariscoord = (48.52, 49.05, 1.97, 2.68)
londoncoord = (51.23, 51.8, -0.50, 0.37)
berlincoord = (52.32, 52.62, 13.11, 13.60)
romecoord = (41.78, 42.0, 12.33, 12.62)
nycoord = (40.25, 40.60, -73.70, -73.40)
spaincoord = (35.12, 43.44, 3.29, 4.22)


bcnigcircles = [(i,j) for i in np.arange(41.30,41.5,0.05) for j in np.arange(2,2.25, 0.05)]

# bcnigcircles = [(41.40, 2.14), (41.46, 2.20), (41.33, 2.07), (41.445, 2.03)]
parisigcircles = [(i,j) for i in np.arange(48.85,49.0,0.05) for j in np.arange(2.15,2.55, 0.05)]

# parisigcircles = [(48.65, 2.33), (48.75, 2.33), (48.85, 2.33), (48.95, 2.33), (49.05, 2.33),
#                   (48.8, 2.45), (48.9, 2.45), (49, 2.45), (48.7, 2.45),
#                   (48.8, 2.21), (48.9, 2.21), (49, 2.21), (48.7, 2.21),
#                   (48.65, 2.09), (48.75, 2.09), (48.85, 2.09), (48.95, 2.09), (49.05, 2.09),
#                   (48.65, 2.57), (48.75, 2.57), (48.85, 2.57), (48.95, 2.57), (49.05, 2.57)]

londonigcircles = [(i,j) for i in np.arange(51.35,51.5,0.05) for j in np.arange(-0.65,0.10,0.05)]
# londonigcircles = [(51.31, -0.07), (51.41, -0.07), (51.51, -0.07), (51.61, -0.07), (51.71, -0.07),
#                    (51.35, 0.05), (51.45, 0.05), (51.55, 0.05), (51.65, 0.05),
#                    (51.35, -0.19), (51.45, -0.19), (51.55, -0.19), (51.65, -0.19),
#                    (51.31, -0.31), (51.41, -0.31), (51.51, -0.31), (51.61, -0.31), (51.71, -0.31),
#                    (51.35, -0.43), (51.45, -0.43), (51.55, -0.43), (51.65, -0.43),
#                    (51.41, 0.17), (51.51, 0.17), (51.61, 0.17),
#                    (51.41, -0.55), (51.51, -0.55), (51.61, -0.55)]
romeigcircles = [(i,j) for i in np.arange(41.75,41.95,0.05) for j in np.arange(12.40,12.7,0.05)]

# romeigcircles = [(41.85, 12.49), (41.95, 12.49), (41.75, 12.49),
#                  (41.80, 12.59), (41.90, 12.59), (41.85, 12.70),
#                  (41.80, 12.39), (41.90, 12.39), (41.80, 12.29)]

berlinigcircles = [(i,j) for i in np.arange(52.42,52.52,0.05) for j in np.arange(12.25,13.60,0.05)]

# berlinigcircles = [(52.52, 13.40), (52.62, 13.40), (52.42, 13.40),
#                    (52.47, 13.30), (52.57, 13.30), (52.37, 13.30),
#                    (52.47, 13.50), (52.57, 13.50), (52.37, 13.50),
#                    (52.52, 13.60), (52.42, 13.60),
#                    (52.52, 13.20), (52.42, 13.20)]

milanigcircles = [(i,j) for i in np.arange(45.45,45.6,0.05) for j in np.arange(9.15, 9.40,0.05)]
# milanigcircles = [(45.46, 9.18), (45.56, 9.18), (45.36, 9.18),
#                   (45.51, 9.28), (45.41, 9.28),
#                   (45.51, 9.08), (45.41, 9.08)]

bcnblacklist = ['LiberateBCN2', 'LiberateBCN2 ','trafficspain06', 'magnesiabcn', 'InformacionDGT', 'trendinaliaBCN', 'EB3TC', 'pisossantcugat', 'BarcelonaVE',
                'Sabadell_Meteo', 'kartenquizde', 'BadalonaCT', 'SabadellES', 'BarcelonaCT', 'Map_Game', 'Fnac_ESP', 'Carutelam', 'ChangeBarcelona', 'Forociudadcom',
                'Carutelam', 'Carutelam ', 'social11red', 'lakasiito_AM', 'tuitrafico_feed', 'oozora_otenki', 'Map_Game', 'TrendsBarcelona', 'trendinalia',
                'tmj_spn_acct', 'segurpricat', 'atrujillo90', 'santboimeteo', 'eltempsasantboi']
milanblacklist = ['TrendsMilano', '_MilanIT', 'TrendsItalia', 'VMwareJobs', 'tami_lovatics', 'tmj_ita_jobs', 'italiaora', 'Map_Game', 'trendinalia',
                  'milanstreaming', 'Nero_Press', 'trendinaliaMXP']
parisblacklist = ['Work_HiltonEMEA', 'remixjobs', 'VideosSexe_net', 'trendinaliaPAR', 'trendinaliaFR', '_ParisFR', 'soltempore', 'tmj_fra_legal',
                  'tmj_fra_itqa', 'tmj_fra_jobs', 'tmj_fra_adv', 'Keys_for_Paris', 'tmj_fra_cler', 'VMwareJobs', 'tmj_fra_itdb', 'BCritique',
                  'QuoteAdo_', 'BCritique ', 'LouAdn2 ', 'LouAdn2', 'Orayane_Models', 'QuoteAdo_ ', 'Nizard_Bdl', 'tmj_fra_hrta', 'trendinalia',
                  'chien_perdu', 'pairsonnalitesF', 'pairsonnalitesN', 'PairsonnalitesU', 'chat_perdu', 'tmj_fra_sales', 'tmj_fra_it',
                  'tmj_fra_itpm', 'PhotoSchedule', 'VeilleDeCM']
londonblacklist = ['trendinaliaGB', 'trendinaliaGB ', 'MWWeather', 'kt19weather', 'Newsminster', 'tmj_lon_jobs', 'ThurrockWeather', 'trendinaliaLON',
                   'ScChouffot', 'kartenquizde', 'arsenalinks', 'footballinks', 'twinklekit', 'MusicNewsWeb', 'VirtualJukebox',
                   'getketo', 'OvergroundBot', 'Work_HiltonEMEA', 'WorkatHilton', 'RPWeather ', 'RPWeather', 'kickalert', 'jxnchanel_',
                   'tmj_LON_secure', 'tmj_LON_adm', 'tmj_lon_adv', 'tmj_lon_finance', 'tmj_lon_eng', 'tmj_lon_retail', 'tmj_LON_facmgmt',
                   'tmj_lon_transp', 'DaiIyLONDON', 'TrafficStAlbans', 'Election20I5', 'ABPhotogra', 'tmj_lon_hrta', 'BroadenMyView',
                   'Map_Game', 'DSBSecurityLTD', 'FaultyBigBen', 'trendinalia', 'BeepBeepTraffic', 'tmj_GBR_skltrd', 'Pairsonnalites',
                   'pairsonnalitesN', 'tmj_GBR_it', 'tmj_lon_itqa', 'tmj_LON_skltrd', 'tmj_LON_actuar', 'tmj_lon_constru',
                   'tmj_lon_hr', 'tmj_lon_itpm', 'tmj_lon_recruit', 'tmj_lon_green', 'tmj_lon_acct', 'tmj_LON_ins', 'tmj_GBR_LEGAL',
                   'tmj_lon_mgmt', 'tmj_lon_pharm', 'tmj_LON_prod', 'tmj_LON_manuf', 'tmj_GBR_EDU', 'tmj_lon_itdb', 'tmj_LON_undrwr',
                   'tmj_GBR_ins', 'tmj_LON_LABOR', '_LondonUK', 'tmj_lon_sales', 'PairsonnalitesU', 'tmj_GBR_HRTA', 'GreenwichLifts',
                   'tmj_lon_legal', 'tmj_LON_itmgmt', 'tmj_LON_cstsrv', 'StockNewsWire', 'TycoCareers', 'BroadbandComUK', 'DerekCopsey',
                   'tdweather', 'soltempore', 'PhotoSchedule', 'CIassicalMusic', 'ch2mjobs', 'infosrv', 'BryanGodfree', 'AndyHerrod',
                   'SolarSchols', 'GrandyOfficial', 'FANTASTICRADIOO', 'O2JobsFeed']
berlinblacklist = ['trendinaliaDE', 'RadioTeddyMusic', '_BB_RADIO_MUSIC', 'pairsonnalitesD', 'pharma24', 'BerlinDE'
                   'dasauge_jobs', 'regenberlin', 'kartenquizde', 'trendinaliaBER', 'tmj_ger_green', 'tmj_ger_ins', 'tmj_ger_itdb',
                   'tmj_ger_art', 'tmj_ger_jobs', 'tmj_ger_itjava', 'tmj_ger_media', 'tmj_ger_edu', 'pinkbigmac', '030_Berlin', 'dasauge_jobs ',
                   'meteo_Berlin', 'tmj_ger_it', '_BerlinDE', 'Map_Game', 'tmj_ger_writing', 'trendinalia', 'cycloppi', 'tmj_ger_itpm']
romeblacklist = ['trendinaliaFCO', 'trendinaliaIT', 'TrendsItalia', 'VaticanVA', 'Rome', 'soltempore', 'luigispaziani1', 'trendinaliaIT ', 'trendinaliaFCO',
                 'TrendsRoma', 'Map_Game', 'tmj_ita_jobs', 'trendinalia', 'pairsonnalitesB', 'PairsonnalitesU', 'TalesToursTips']

bcnparam = (mgdbbcn, bcncoord, 'bcn', bcnigcircles, 360, set(bcnblacklist))
milanparam = (mgdbmilan, milancoord, 'milan', milanigcircles, 360, set(milanblacklist))
hlsnkparam = (mgdbhelsinki, hlsnkcoord, 'hlsnk')
parisparam = (None, pariscoord, 'paris', parisigcircles,240, set(parisblacklist))
londonparam = (None, londoncoord, 'london', londonigcircles, 240, set(londonblacklist))
berlinparam = (None, berlincoord, 'berlin', berlinigcircles, 360, set(berlinblacklist))
romeparam = (None, romecoord, 'rome', romeigcircles, 360, set(romeblacklist))
spainparam= ('ES', spaincoord, 'spain', None, 0, set())
nyparam = (None, nycoord, 'newyork', None, 300, set())

cityparams = {
    'bcn': bcnparam,
    'milan': milanparam,
    'paris': parisparam,
    'london': londonparam,
    'berlin': berlinparam,
    'rome': romeparam,
    'spain': spainparam,
    'newyork': nyparam
}

TW_TIMEOUT = 3600  # 1 hour
IG_TIMEOUT = 300  # 5 minutes