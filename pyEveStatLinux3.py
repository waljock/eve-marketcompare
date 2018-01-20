# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 12:49:12 2017

@author: Walter
"""

import pandas as pd
import os
import urllib3
import certifi



import datetime, time


xlTypes = ('invTypes.xls')
systems = ('mapSolarSystems.csv')


ssNames = ['Jita', 'GE-8JV', '68FT-6']

"""
Collect Inventory Types and Filter for what we want

"""

p2xl0 = pd.read_excel(r"invTypes.xls", sheet_name='Sheet1')

p2xl =p2xl0[(p2xl0['MARKETGROUPID']>=1) & (p2xl0['MASS'] >= 0) & (p2xl0['MASS'] <= 5)].head(500)

#make a lsit of Type Codes that we will analyze

codelst = list(p2xl['TYPEID'])
"""


Read in System Info and Station Info from Static File 


"""
statSS = pd.read_csv(systems, usecols = ['regionID',  'constellationID',  'solarSystemID',
                                          'solarSystemName'])

statSSlst = statSS[statSS['solarSystemName'].isin(ssNames)]



#startup URLLIB

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())



for i in range(0, len(codelst)):#m21)):
    


    url3 = "https://esi.tech.ccp.is/latest/markets/10000002/history/?datasource=tranquility&type_id=" + str(codelst[i]) 
    r3 = http.request("GET",url3)
    stat3 = r3.status
    data3 = r3.data
    
    
    
    try:
        m3 = pd.read_json(data3).tail(50)
 #       m3['type_id'] = avgTypes[i]
        m30 = pd.DataFrame(m3, columns=('type_id', 'average'))
        m31 = m30.groupby('type_id').mean()
        m32 = m31.reset_index()
        """
        m33 = pd.merge(m21, m32)
        m34 = m33[(m33['average_price'] <= m33['average'])]
        
        data_all.append(m34)
        """
    except:
        pass
'''    
data_all = pd.concat(data_all, ignore_index=False)   

dfafin = pd.merge(data_all, p2xl, left_on='type_id', right_on='TYPEID') 

dfafin['pct'] = dfafin['average']/dfafin['average_price']

final = dfafin[(dfafin['pct']>=3)]

final.to_excel("test.xlsx")
'''
#url = "https://esi.tech.ccp.is/latest/markets/prices/?datasource=tranquility"
#
#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#r = http.request("GET",url)
#stat = r.status
#data = r.data
#m2 = pd.read_json(data)
#m21 = m2[(m2['average_price']>=100000) & (m2['average_price']<=5000000)]
#
#avgTypes = m21['type_id'].tolist()
#
#dis ={'adjusted_price':[], 'average_price':[], 'type_id':[], 'average':[]}
#df = pd.DataFrame(columns=('adjusted_price', 'average_price', 'type_id', 'average'))
##qry = market[market["type_id"] == 18]
#df['datestamp'] = pd.to_datetime('today')
#
#appe =[]
#
#data_all = []
#
##I'd like to put this into a data base

#Set len below to low number to test
    #appe = pd.concat(appe, axis=1)

 
#    dis.update(y)
#    df.append(m34, ignore_index=True)

#file1 = os.path(path1,xlTypes)



#https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility
