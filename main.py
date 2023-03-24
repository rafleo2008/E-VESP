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
from pathlib import Path


#### Main paths and directions

timeTablesPath = Path("Intermediate/timetables.csv")

#### Main functions

def calculateTimeTables(route, RSP, REP, STime, ETime, Frequency):
    
    print("Calculating departure times")
    timeTable = pd.DataFrame(columns = ["Route","RSP","REP","DepTime"])
    
    intervalMin = timedelta(minutes = (60/Frequency))

    depTime = STime

    
    while(depTime <= ETime):
        line = pd.DataFrame([[route, RSP, REP, depTime]],
                            columns = ["Route","RSP","REP","DepTime"])
        #print(line)
        depTime = depTime+intervalMin
        timeTable = pd.concat([timeTable, line])
    return timeTable
    

#### Main Code

#Load timetable example

timeTable = pd.read_csv("Inputs\Frequencies_csv.csv",
                        parse_dates = ['HourFrom', "HourTo"] )


##
compiledTimeTable = pd.DataFrame(columns = ["Route","RSP","REP","DepTime"])

for row in timeTable.iterrows():
    curRoute = row[1].Route
    curRSP = row[1].Origin
    curREP = row[1].Destination
    curSTime = row[1].HourFrom
    curETime = row[1].HourTo
    curFreq = row[1].Frequency
    
    myTimeTable = calculateTimeTables(curRoute, curRSP, curREP, curSTime,
                        curETime, curFreq)
    print(myTimeTable)
    compiledTimeTable = pd.concat([compiledTimeTable, myTimeTable])


print(len(compiledTimeTable))
       
compiledTimeTable.to_csv(timeTablesPath)    
    



    

#print(timeTable)
## Load functions
## Load vehicles


