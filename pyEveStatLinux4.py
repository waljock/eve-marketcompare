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

test = ('test.xlsx')



ssNames = ['Jita', 'GE-8JV', '68FT-6']

"""
Collect Inventory Types and Filter for what we want

"""

p2xl0 = pd.read_excel(test, sheet_name='Sheet1')
types = pd.read_excel(xlTypes, sheet_name='Sheet1')

p2xl =p2xl0#[(p2xl0['GROUPID'] == 25)]

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

for i in range(0, len(codelst)):#m21)):
    


    url3 = "https://esi.tech.ccp.is/latest/markets/10000002/history/?datasource=tranquility&type_id=" + str(codelst[i]) 
    r3 = http.request("GET",url3)
    stat3 = r3.status
    data3 = r3.data
    
    
    url4 = "https://esi.tech.ccp.is/latest/markets/10000014/history/?datasource=tranquility&type_id=" + str(codelst[i]) 
    r4 = http.request("GET",url4)
    stat4 = r4.status
    data4 = r4.data
    

    
    
    
    try:
        m3 = pd.read_json(data3)
        m3['type_id'] = codelst[i]
        m30 = pd.DataFrame(m3, columns=('type_id', 'average'))
        m31 = m30.groupby('type_id').mean()
        m32 = m31.reset_index()
        m32['region'] = 'Jita'
        print("data for Jita " + str(codelst[i])) # + " received:  " + str(m32['TYPENAME'].head(1)) )
     
        #m33 = pd.merge(m21, m32)
        #m34 = m33[(m33['average_price'] <= m33['average'])]
        
        data_all.append(m32)
        
        m4 = pd.read_json(data4)
        m4['type_id'] = codelst[i]
        m40 = pd.DataFrame(m4, columns=('type_id', 'average'))
        m41 = m40.groupby('type_id').mean()
        m42 = m41.reset_index()
        m42['region'] = 'Catch'
        print("data for Catch " + str(codelst[i])) # + " received:  " + str(m42['TYPENAME'].head(1)) )
        
        data_all2.append(m42)
       
    except:
        pass
    
    
    
data_all = pd.concat(data_all, ignore_index=False)   
data_all2 = pd.concat(data_all2, ignore_index=False)   

data_all3 = data_all2.append(data_all)
#
#dfafin = pd.merge(data_all, p2xl, left_on='type_id', right_on='TYPEID') 
#dfafin2 = pd.merge(data_all2, p2xl, left_on='type_id', right_on='TYPEID') 

#
#dfafin.to_excel("Jita.xlsx")
#dfafin2.to_excel("Catch.xlsx")
data_all3.to_excel("combined_data.xlsx")


