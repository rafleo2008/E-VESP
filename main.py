# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 21:03:05 2022
@author: Rafael Munoz


"""
## ------------------------------------------------------------------------- ##
## Code description




## Import required modules

import pandas as pd
import geopandas as gpd
import time
from datetime import timedelta
from pathlib import Path


#### Main paths

routeFrequPath = Path("Inputs/Frequencies_csv.csv")
timeTablesPath = Path("Intermediate/timetables.csv")

#### Main variables
dateFormat = "&H:$M"

# Define the custom date parser function
dateParser = lambda x: pd.to_datetime(x, format=dateFormat)


#### Main functions (This should be moved away, this is the compile code)

def calculateTimeTables(route, RSP, REP, STime, ETime, Frequency):
    
    print("Calculating departure times")
    timeTable = pd.DataFrame(columns = ["Route","RSP","REP","DepTime"])
    
    intervalMin = timedelta(minutes = (60/Frequency))

    depTime = STime

    
    while(depTime < ETime):
        line = pd.DataFrame([[route, RSP, REP, depTime]],
                            columns = ["Route","RSP","REP","DepTime"])
        #print(line)
        depTime = depTime+intervalMin
        timeTable = pd.concat([timeTable, line])
    return timeTable
    

#### Main Code

#Load timetable example

timeTable = pd.read_csv(routeFrequPath, 
                        parse_dates = ['HourFrom', "HourTo"],
                        #date_parser=dateParser
                        )


## Create an empty DF to store new scheduling
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

#compiledTimeTable.set_index(list(range(len(compiledTimeTable))), inplace = True)

       
compiledTimeTable.to_csv(timeTablesPath)    
    

    

#print(timeTable)
## Load functions
## Load vehicles


