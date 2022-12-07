# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 18:43:09 2022

@author: rafle
"""

import pandas as pd
import datetime as dt
from datetime import timedelta
from datetime import datetime

freq =pd.read_csv("DepTimes/Inputs/FreqExample.csv")

## Set Times in datetime format

freq['Start_Time']= pd.to_datetime(freq['Start_Time'])
freq['End_Time']= pd.to_datetime(freq['End_Time'])

## Filter routes
routes = freq['Route'].unique()

### 


depTimes = []
    
for route in routes:
    # Filter route's start point 
    routeFreq = freq[freq['Route']==route]
    StartPoints = routeFreq['Start_Point'].unique()
    print(StartPoints)
    
    for StartPoint in StartPoints:
        ## Loop for tabletime
        routeStartPoint = routeFreq[routeFreq['Start_Point']== StartPoint]
        ## Set start, end time and Services
        
        serviceCounter = 1
        startTime = routeStartPoint['Start_Time'].min()
        endTime = routeStartPoint['End_Time'].max()
        totServices = routeStartPoint['Frequency'].sum()
        
        for line in routeStartPoint.iterrows():
            hourFreq = line[1]['Frequency']
            blockStartTime = datetime.timestamp(line[1]['Start_Time'])
            blockEndTime = datetime.timestamp(line[1]['End_Time'])            
            print(blockStartTime)
            #blockStartTime = line[1]['Start_Time']
            interval = (blockEndTime -blockStartTime)/60
            timeInt = (interval/hourFreq)*60
            blockTime = blockStartTime
            while blockTime < blockEndTime:
                container = []
                route = line[1]['Route']
                depot = line[1]['Depot']
                starP = line[1]['Start_Point']
                despT = blockTime
                container.append(route)
                container.append(depot)
                container.append(starP)
                container.append(despT)
                
                depTimes.append(container)
                print(depTimes)                
                blockTime = blockTime +timeInt

depDataFrame = pd.DataFrame(depTimes, 
                            columns = ['Route','Depot','Start_Point','Dep_Time'])
depDataFrame.to_csv('Ejemplo.csv')     
                
            

        
       
        
            
            
            
        
    
 


