# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:29:26 2023

@author: rafle
"""



'''
MODEL DESCRIPTION

This model aims to assess the compatibility of a bus 
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
    1.3. If Charged, Keep position and no charge
    1.4. If going to PIR: Navigate from Bus Depot to PIR and discharge
    1.5. If InRoute: Navigate along the route and discharge, Update SOC, Calculate remaining Km.
    1.6. If going to bus depot: Navigate and discharge.
    

    
'''
## Functions
def runModel(startTime, endTime, simResolution, reportFreq, fleet, myTimeTable):
    ## Initialize time control variables
    print("Simulation run starts")
    simStep = startTime
    counter = 0
    minuteStep = simResolution
    row = 0
    i = 0
    #minuteStep = simResolution.total_seconds()/60
    
    ## Initialize vehicles, PIR and controllers
    for bus in fleet:
        bus.assignStatus("Parked")
    
    while(simStep <=endTime):
        ## Time loop, here, the model will run in each step
        

        
        ## All objects actions (busses, controllers, buscontroller)
        
        # Cannot use speed, tag speed using controller
        # This should be inside a batch to run all busses at once

        for bus in fleet:
            #print(bus.status)
            bus.runStep(minuteStep,60)

        #NorthPIR.runStep(simStep,m.myTimeTable)
        ## Report 
        if (counter%reportFreq == 0):
            # This could be also a function
            print("Reporte del paso " + str(simStep))
            for bus in fleet:
                print(bus.busId + " - Estado : "+ bus.status + "SoC: " + str(bus.soc) + " - Odometer: " + str(bus.odo))
        
                
        ## Simulate in-route bus at step 300
        '''
        if (simStep == 300):
            ## Status tests
            fleet[5].assignStatus("InRoute")
        '''
        
        
        departure = myTimeTable.iloc[row]
        #print(departure)

        if(simStep == departure.TimeStep):
            print("Departure simstep " + str(simStep))
            fleet[i].assignStatus("InRoute")
            row = row + 1
            i = i + 1
            
        
            
        
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
from datetime import datetime

from datetime import timedelta
import objects as o
import pandas as pd

## Default input parameters

## Base parameters, pending to convert to todays parameters
## start and end hour should be user inputs


### Start new simulation step procedure

start_day = 0
start_hour = 0
start_minute = 0

end_day = 1
end_hour = 0
end_minute = 0

min_time_step = 1

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

n = 34 # further input variable

fleet = []


for i in range(n):
    busId = f"Ebus_E{i:02d}"
    
    print("Creando bus " + busId)
    bus = o.eBus('Sunwin', 
                 'EVB8m',
                 2023,
                 250,
                 True, 
                 0.9,
                 0.75, 
                 1, 
                 0.85, 
                 0,
                 busId)
    
    fleet.append(bus)
    
for bus in fleet:
    
    print(bus.busId)

## Open timetable

 
# Enviar esto a main
myTimeTable = m.compiledTimeTable
myTimeTable["DepTime"] = pd.to_datetime(myTimeTable["DepTime"])
#reference_time = pd.Timestamp('2024-05-21 00:00:00')

today = pd.Timestamp(datetime.now().date())
reference_time = today

myTimeTable["TimeStep"] = (myTimeTable["DepTime"] - reference_time).dt.total_seconds() // 60


print(myTimeTable)


   
## Run Model

runModel(start_min_step, end_min_step, min_time_step, 60, fleet, myTimeTable)




