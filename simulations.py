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
    minuteStep = simResolution
    #minuteStep = simResolution.total_seconds()/60
    
    ## Initialize vehicles, PIR and controllers
    
    while(simStep <=endTime):
        ## All objects actions (busses, controllers, buscontroller)
        
        # Cannot use speed, tag speed using controller
        # This should be inside a batch to run all busses at once
        for bus in fleet:
            bus.runStep(minuteStep,10)

        NorthPIR.runStep(simStep ,m.myTimeTable)
        ## Report 
        if (counter%reportFreq == 0):
            # This could be also a function
            print(simStep)
            #print(o.bus1.soc)
            #print(o.bus1.odo)
        ##
        counter = counter + 1
        simStep = simStep + simResolution

def dateToTimeStep(day, hour, minute):
    ## Convert day, hour and minute to timesteps
    timeStep = day*(60*24) + hour*60 + minute
    return timeStep        
def timeStepToDate(timeStep):
    days = timeStep//(60*24)
    rem = timeStep - (days*1440)
    hours = rem//60
    rem = (rem - (hours*60))
    minutes = rem
    print("{0} steps are {1} days, {2} hours and {3} minutes".format(timeStep, days, hours, minutes))
    return days, hours, minutes
    #hours = (timeSteps%(60*24))/24
    #minute = ((timeSteps%(60*24))/24)
    
               
## Import main libraries

import main as m
import time
from datetime import datetime as dt
from datetime import timedelta
import objects as o

## Default input parameters

## Base parameters, pending to convert to todays parameters
## start and end hour should be user inputs


### Start new simulation step procedure

start_day = 0
start_hour = 0
start_minute = 0

end_day = 3
end_hour = 0
end_minute = 0

min_time_step = 5

start_min_step = dateToTimeStep(start_day, start_hour, start_minute)
end_min_step = dateToTimeStep (end_day, end_hour, end_minute)



print("Simulation start at {} timesteps".format(start_min_step))
print("Simulation end at {} timesteps".format(end_min_step))

### End new simulation step procedure

##  PIR Definitions

NorthPIR = o.PIR("North", "A1", "Depot1")
SouthPIR = o.PIR("South", "A1", "Depot1")

## Create Bus Fleet (Specific size)
## Further development will include a default bus fleet calculation

n = 38 # further input variable

fleet = []

for i in range(n):
    bus = o.eBus('Sunwin','EVB8m',2023,250, 0.9,0.75, 1,0, 85, 0)
    fleet.append(bus)
    
for bus in fleet:
    
    print(bus.brand)
   
## Run Model

runModel(start_min_step, end_min_step, min_time_step, 48)

'''
for i in (range(50)):
    print(bus_fleet.brand)
'''