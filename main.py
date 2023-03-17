# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 21:03:05 2022
@author: Rafael Munoz
"""
#

## Import required modules

import pandas as pd
import geopandas as gpd
import time
from datetime import timedelta

## Main functions
def calculateTimeTables(route, RSP, REP, STime, ETime, Frequency):
    timeTable = pd.DataFrame(columns = ["Route","RSP","REP","DepTime"])
    print("Running calculate Time Tables")
    intervalMin = timedelta(minutes = (60/Frequency))
    depTime = STime
    print(STime)
    
    while(depTime <= ETime):
        line = pd.DataFrame([[route, RSP, REP, depTime]],
                            columns = ["Route","RSP","REP","DepTime"])
        print(line)
        depTime = depTime+intervalMin
        timeTable = pd.concat([timeTable, line])
        #timeTable = timeTable.append(line)
    return timeTable
    

## Load timetable example

timeTable = pd.read_csv("Inputs\Frequencies_csv.csv",
                        parse_dates = ['HourFrom', "HourTo"] )

## 


##
for row in timeTable.iterrows():
    curRoute = row[1].Route
    curRSP = row[1].Origin
    curREP = row[1].Destination
    curSTime = row[1].HourFrom
    curETime = row[1].HourTo
    curFreq = row[1].Frequency
    
    myTimeTable = calculateTimeTables(curRoute, curRSP, curREP, curSTime,
                        curETime, curFreq)
       
myTimeTable.to_csv("Intermediate\timetables.csv")    
    
    

    

#print(timeTable)
## Load functions
## Load vehicles


