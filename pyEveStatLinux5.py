# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 12:49:12 2017

@author: Walter
"""

import pandas as pd
import os
import urllib3
import certifi
#import h5py






import datetime, time



#read Static data

xlTypes = ('invTypes.xls')
systems = ('mapSolarSystems.csv')



#read file generated from lin2

ssNames = ['Jita', 'GE-8JV', '68FT-6']

"""
Collect Inventory Types and Filter for what we want

"""


types = pd.read_excel(xlTypes, sheet_name='Sheet1')

p2xl =types[(types['BASEPRICE'] >= 1)]

#make a lsit of Type Codes that we will analyze

codelst = list(p2xl['TYPEID'])
"""


Read in System Info and Station Info from Static File 


"""
statSS = pd.read_csv(systems, usecols = ['regionID',  'constellationID',  'solarSystemID',
                                          'solarSystemName'])

statSSlst = statSS[statSS['solarSystemName'].isin(ssNames)]

#store = pd.HDFStore('eve-store.h5')
#store['types'] = types
#store['systems']=statSS
#store['freshdata'] = p2xl


#startup URLLIB

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

data_all = []
data_all2 = []

for i in range(0, 200):
    
#look up catch prices
    
    url4 = "https://esi.tech.ccp.is/latest/markets/10000014/history/?datasource=tranquility&type_id=" + str(codelst[i]) 
    r4 = http.request("GET",url4)
    stat4 = r4.status
    data4 = r4.data
    
    try:
    
        m4 = pd.read_json(data4)
        m4['type_id'] = codelst[i]
        m40 = pd.DataFrame(m4)
        m41 = m40#.groupby('type_id').mean()
        m42 = m41.reset_index()
        m42['region'] = 'Catch'
        print("data for Catch " + str(codelst[i])) # + " received:  " + str(m42['TYPENAME'].head(1)) )
        
        data_all2.append(m42)
        
    except:
       pass

data_all2 = pd.concat(data_all2, ignore_index=False)   

cfilter = data_all2[(data_all2['date'] >= '2017-12-01')]

recency = cfilter.filter(['type_id','order_count','average', 'volume'])
recgrp = recency.groupby('type_id').mean()
recgrp2 = recgrp.reset_index() 

recgrp3 = recgrp2.rename(columns={'type_id':'Ctype','order_count':'Corders','average':'Cprice', 'volume':'Cvolume'})

t = list(recgrp3['Ctype'])

for y in range(0,len(t)):
#Jita is 10000002 , Catch is 10000014, Dodixie 10000032
    

    url3 = "https://esi.tech.ccp.is/latest/markets/10000002/history/?datasource=tranquility&type_id=" + str(t[y]) 
    r3 = http.request("GET",url3)
    stat3 = r3.status
    data3 = r3.data

    
    
    try:
        m3 = pd.read_json(data3)
        m3['type_id'] = t[y]
        m30 = pd.DataFrame(m3)
        m31 = m30#.groupby('type_id').mean()
        m32 = m31.reset_index()
        m32['region'] = 'Jita'
        print("data for Jita " + str(t[y])) # + " received:  " + str(m32['TYPENAME'].head(1)) )
     
        #m33 = pd.merge(m21, m32)
        #m34 = m33[(m33['average_price'] <= m33['average'])]
        
        data_all.append(m32)

#       
    except:
        pass
#    
#    
#    
data_all = pd.concat(data_all, ignore_index=False)   

jfilter = data_all[(data_all['date'] >= '2018-01-01')]


jrecency = jfilter.filter(['order_count','average', 'type_id', 'volume'])
jrecgrp = jrecency.groupby(['type_id']).mean()
jrecgrp2 = jrecgrp.reset_index() 

jrecgrp3 = jrecgrp2.rename(columns={'type_id':'Jtype','order_count':'Jorders','average':'Jprice','volume':'Jvolume'})

m = pd.merge(jrecgrp3, recgrp3, left_on = 'Jtype', right_on = 'Ctype')

n = pd.merge(m, types, left_on = 'Jtype', right_on = 'TYPEID', how='left')

n['pct'] = n['Cprice']/n['Jprice']


n.to_csv('CatchJita.csv')
#data_all2 = pd.concat(data_all2, ignore_index=False)   
#
#data_all3 = data_all2.append(data_all)
##
##dfafin = pd.merge(data_all, p2xl, left_on='type_id', right_on='TYPEID') 
##dfafin2 = pd.merge(data_all2, p2xl, left_on='type_id', right_on='TYPEID') 
#
##
##dfafin.to_excel("Jita.xlsx")
##dfafin2.to_excel("Catch.xlsx")
#data_all3.to_excel("combined_data.xlsx")
#
#
