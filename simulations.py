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
def runModel(startTime, endTime, simResolution, reportFreq, fleet, myTimeTable, logs):
    '''
    This function run the model from start time to end time, at each sim resolution,
    reports every report freq (steps) and use the fleet and timetable to interact
    
    Parameters
    startTime: int
    endTime: int
    simResolution: int
    reportFreq: int
    fleet: list containing bus elements
    timeTable: dataframe
    ## To be implemented 
    line(s): geodataframe
    
     
    '''
    ## 01. Initialize time control variables
    global log
    global busResults
    log = printAndCompileMsg("RunModel function starts", 
                             log)

    simStep = startTime
    counter = 0
    minuteStep = simResolution
    row = 0
    rowA = 0
    i = 0
    #minuteStep = simResolution.total_seconds()/60
    
    ## 02. Initialize vehicles, PIR and controllers
    for bus in fleet:
        # Define innital location of buses
        bus.setInitialLocation('Bus depot', 'Depot A')
        # Define innital status
        bus.assignStatus("Parked")
        # Save in log the created buses register
        log = printAndCompileMsg(str(simStep)+', '+ bus.busId + " parked",
                                 log)
    
    while(simStep <=endTime):
        ## Time loop, here, the model will run in each step   
        ## All objects actions (busses, controllers, buscontroller)
        
        ## Identify need in advance of busses
        
        timeToPir = math.ceil((5/17)*60) # time from bus depot to PIR in minutes
        
        ## 01. Check for need to departure busses from bus depot to PIR
        
        for bus in fleet:
            bus.runStep(minuteStep,60, simStep)

        ## Generate report        
        if (counter%reportFreq == 0):
            
            # This could be also a function

            for bus in fleet:

                log = printAndCompileMsg(str(simStep)+ "," + 
                                         bus.busId + ", Estado :"+
                                         bus.status + ", SoC: " +
                                         str(bus.soc) + ", Odometer: " +
                                         str(bus.odo) + ", routepos: " +
                                         str(bus.routePosit) + ",No trips: "+
                                         str(bus.tripscounter)+ ",Route len: "+
                                         str(bus.routeLengt), 
                                         log)

                busResults.append([simStep,
                                   bus.busId,
                                   bus.status,
                                   bus.soc,
                                   bus.odo,
                                   bus.routePosit,
                                   bus.tripscounter])

        ## Check bus availability
        availableInDepot = []       # Available buses in depot
        availableInPIR = []
        toBeAvailableinPIR = []
        
        countAvaiDep = 0
        countAvaiPIR = 0
        countToBeAva = 0                            
        
        # Loop checking availability
        
        fleetCount = 0
        
        for bus in fleet:
            # Check if bus is available at depot
            if bus.status == 'Parked' and bus.soc >= (250*.1)+(22*.9):
                availableInDepot.append(fleetCount)
                #print(str(len(availableInDepot))  +'veh en el patio')
            # Check which buses are available at PIR
            elif bus.status == 'AvailableInPIR':
                availableInPIR.append(fleetCount)
                #print(str(len(availableInPIR))  +'veh en el PIR')
            # Check wich buses will be availabe at future dep Time
            elif (bus.status == 'InRoute' and (bus.routeLengt - bus.routePosit <= 0.5) and bus.soc >= (250*.1)+(27*.9)):
                toBeAvailableinPIR.append(fleetCount)
            
                #print(str(len(toBeAvailableinPIR))  +'A LEGAR AL PIR')

            fleetCount = fleetCount + 1
        
        # Dispatch to PIR if there's no future available busses
        
        #Bring timetable

        ## Send buses back to bus depot if there are no more dispaths
        if myTimeTable.shape[0] == row:
            print(simStep)

            print("No more dispatches, send available buses to bus depot")
            # Check if we have buses available in pir, then send to bus depot
            if len(availableInPIR) > 0:
                for busId in availableInPIR:
                    fleet[busId].assignStatus('ReturnToDepot')
        
        ## Depart if there are available dispatch
        
        if myTimeTable.shape[0] > row:
            
            depBusdep = myTimeTable.iloc[rowA]
            departure = myTimeTable.iloc[row]
        
            # Dispatch to PIR
            if(simStep == (round(depBusdep.TimeStep,0) - timeToPir - 1)):
                # Check if there is any vehicle to arrive at PIR
                if len(toBeAvailableinPIR) == 0:
                    print("At "+ str(simStep) +", send a bus to InRoute"+ fleet[availableInDepot[0]].busId)
                    fleet[availableInDepot[0]].innitializeRoute()
                    fleet[availableInDepot[0]].assignStatus("InTransit")
                    rowA = rowA + 1

            
            # Dispatch in PIR
            
            if(simStep == departure.TimeStep):  #Fleet assignment
                print("Departure simstep " + str(simStep))
                print("Hay " +str(len(availableInPIR))+" buses disponibles")
                fleet[availableInPIR[0]].assignStatus("InRoute")
                fleet[availableInPIR[0]].innitializeRoute()
                print("Bus no "+ fleet[availableInPIR[0]].busId +" ha inicado ruta en el simStep" + str(simStep))
                row = row + 1

                
       
        # Send parked and discharged buses to charge
        busCount = 0
        for bus in fleet:
            if bus.status == "Parked" and bus.soc <= (250*.1)+(22*.9):
                fleet[busCount].assignStatus("Charging")
                fleet[busCount].restartRoutePosit()
            busCount = busCount +1
        

        
        # Next steps
        
        counter = counter + 1
        simStep = simStep + simResolution
        
    
    ## Close logfile
    
    with open("logfile.txt", "w") as output:
        output.write(str(logs))

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
def printAndCompileMsg(text, log):
    print(text)
    log.append(text)
    return log

def writeMessages(log):
    with open('results.txt', 'w') as f:
        for message in log:
            f.write(message + '\n')
    
    
               
## Import main libraries

import main as m
import time
from datetime import datetime

from datetime import timedelta
import objects as o
import pandas as pd
import math
from pathlib import Path


## General preparation codes
## Open timetables
timeTablesPath = Path("Intermediate/timetables.csv")

compiledTimeTable = pd.read_csv(timeTablesPath)

## 01. Set time parameters (to be replaced by an environment set up)
## 01.1. Start time
start_day = 0
start_hour = 0
start_minute = 0

## 01.2. End Time

end_day = 1
end_hour = 0
end_minute = 0

## 01.3. Set time step (minimal discrete simulation interval (minutes))

min_time_step = 1

## 02. Configure start and end timestep

start_min_step = dateToTimeStep(start_day, start_hour, start_minute)
end_min_step = dateToTimeStep (end_day, end_hour, end_minute)

## 03. Setting up log and results files
log = []
busResults = []
## 03.1. Setting up results file
busResultsHeaders = ['TimeStep',
                    'Bus_Id',
                    'Status',
                    'SoC',
                    'Odometer',
                    'Route_Position',
                    'Trips_Completed'
    ]

## 04. Innitialization messages

log = printAndCompileMsg("Model starts running", log)
log = printAndCompileMsg("Simulation start at {} timesteps".format(start_min_step), 
                         log)
log = printAndCompileMsg("Simulation end at {} timesteps".format(end_min_step), 
                         log)

## 04. Create input data (To be replaced by an environment set up)
## 04.1. Route settings 
## 04.1.1. Bus Depot data

NorthPIR = o.PIR("North", "A1", "Depot1")
SouthPIR = o.PIR("South", "A1", "Depot1")

## 04.1.2. Bus fleet definition

n = 16 # further input variable, further development will include validation

fleet = []

for i in range(n):
    busId = f"Ebus_E{i:02d}"
    log = printAndCompileMsg("Creando bus " + busId, log)
    
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

log = printAndCompileMsg("Created vehicles in fleet", log)

## Open timetable

 
# Enviar esto a main
myTimeTable = compiledTimeTable
myTimeTable["DepTime"] = pd.to_datetime(myTimeTable["DepTime"])
#reference_time = pd.Timestamp('2024-05-21 00:00:00')

today = pd.Timestamp(datetime.now().date())
reference_time = today

myTimeTable["TimeStep"] = (myTimeTable["DepTime"] - reference_time).dt.total_seconds() // 60


print(myTimeTable)


   
## 05. Run Model

## Create route data

## Route example
routeA = {'name': "Route A",
          'NoBusDep': 1,
          'DepNames':['DepotA'],
          'DepCoord':[[0,0]]}

runModel(start_min_step, end_min_step, min_time_step, 1, fleet, myTimeTable, log)

## 06. Write results


writeMessages(log)

busResultsDF = pd.DataFrame(data = busResults, columns = busResultsHeaders)
busResultsDF.to_csv("BUs_results.csv")
log = printAndCompileMsg("Run finalized correctly", log)