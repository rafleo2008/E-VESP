# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:29:26 2023

@author: rafle
"""



'''
MODEL DESCRIPTION

This model aims to assess, at strategic level, the compatibility of a bus 
operation system with specific e-bus model.

The application of this model will expand the model potential, with the ability
of assess operation along the years, including battery degradation and change
in operational schemes due to less range.

Desceription:
    1. Load route(s) and calculate basic parameters (cycle time) (create object?)
    2. Load PIRs
    3. Define bus fleet based on 
        1. Operative design (MaxFreq/Tc)
        2. Single bus model or custom list
    4. Calculate specific E-bus parameters
        1. 

Once all has been set up, run the model
The model assess a typical day in small time segments (1 minute, for example)
At every step, every object perform specific actions.

EBus
    1. Check status
    1.1. If parked: Do nothing
    1.2. If charging: Keep position and Use charging curve to update 
        Soc and Battery
    1.3. If going to PIR: Navigate from Bus Depot to PIR and discharge
    1.4. If Navigating: Navigate along the route and discharge, Update SOC, Calculate remaining Km.
    1.5. If going to bus depot: Navigate and discharge.
'''
## Functions
def runModel(startTime, endTime, simResolution, reportFreq):
    ## Initialize time control variables
    
    simStep = startTime
    counter = 0
    minuteStep = simResolution.total_seconds()/60
    
    ## Initialize vehicles, PIR and controllers
    
    
    while(simStep <=endTime):
        ## All objects actions (busses, controllers, buscontroller)
        
        # Cannot use speed, tag speed using controller
        # This should be inside a batch to run all busses at once
        o.bus1.runStep(minuteStep, 10)
        ## Report 
        if (counter%reportFreq == 0):
            # This could be also a function
            print(simStep)
            print(o.bus1.soc)
            print(o.bus1.odo)
        ##
        counter = counter + 1
        simStep = simStep + simResolution
        
               
## Import main libraries

import main as m
import time
from datetime import datetime as dt
from datetime import timedelta
import objects as o

## Default input parameters

## Base parameters, pending to convert to todays parameters
## start and end hour should be user inputs

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

o.bus1.setInitialBattery(1.5)


## Run Model

runModel(startTime, endTime, simResolution, 6)


