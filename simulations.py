# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:29:26 2023

@author: rafle
"""

## Loop

import main as m
import time
from datetime import datetime as dt
from datetime import timedelta
import objects as o

#print(m.compiledTimeTable)

## Default imputs
startYear =2023
startMonth = 3
startDay = 20
startHour= 5
endHour = 0
startTime = dt(year = startYear,
               month = startMonth,
               day = startDay,
               hour = startHour)
endTime = dt(year = startYear,
             month = startMonth,
             day = startDay+1,
             hour = endHour)

simResolution = timedelta(minutes = 5)

## Sim Time
print(o.bus1.model)
print(o.bus1.consAC)

simStep = startTime


while (simStep <= endTime):
    if simStep.minute%15 == 0:      
        print(simStep)
        print(o.bus1.soc)
        print(o.bus1.odo)
    ## Run simulations
    #print(simStep)
    minuteStep = simResolution.total_seconds()/60
    #print(minuteStep)
    o.bus1.runStep(minuteStep, 30)
    #print(o.bus1.odo)
    ## Visualization routine
    

    
    simStep = simStep + simResolution