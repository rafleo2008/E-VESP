# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:42:01 2023

@author: rafle
"""
## Main modules

from datetime import timedelta

## Objects definition

## ebus



class eBus:
    ## Initial default values
    fleet = []
    
    def __init__(self, 
                 brand: str,
                 model: str,
                 year: int, #Delete?
                 capacity: float, 
                 ac: bool, # change name
                 consAC: float,
                 consNoAC: float,
                 soc: float,
                 socpe: float,
                 odo: float):
        
        ## Assign self initial parameters
        
        self.brand = brand
        self.model = model
        self.year = year
        self.capacity = capacity
        self.ac = ac
        self.consAC = consAC
        self.consNoAC = consNoAC
        self.odo = odo
        self.soc = capacity
        
        ## Actions
        eBus.fleet.append(self)
        
    
    def setInitialBattery(self,charge):
        self.soc = min(self.capacity, (charge*self.soc))
        self.socpe = self.soc/self.capacity
        print("The battery has been defined as {} kWh, {} % of the battery".format(str(self.soc),
                                                                                   str(self.socpe)))             

    def assignStatus(self, status):
        self.status = status
        

    def runStep(self, step, speed):
                
        currentStatus = self.status
        energy = step*speed
        #print(energy)
        
        '''
        
        Bus activity based in the status:
        Status
        - Parked = Parked in the 
        Check status
        
        If charging, add current to battery until reach capacity
        If in transit, discharge at specific rate and displace to a new point in the route
        '''
        
        
        self.odo = self.odo + speed*(step/60)
        self.soc = self.soc - (speed*(step/60))*self.consAC
    
    def printStatus(self):
        print("Bus status : {}".format(self.status))
        #print("SOC = ")
        
## dispatcher        

class PIR:
    pirs = []
    def __init__(self, 
                 place : str,
                 routes: [],
                 depots: [],
                 lookaheadtime = int):
        self.place = place
        self.routes = routes
        self.depots = depots
        self.lookaheadtime = lookaheadtime
        
        # Actions
        PIR.pirs.append(self)
    def runStep(self, step):
        '''
        Check all timesteps (at minute) and check if theres a departure time
        If theres a departure time, assign ebus from list

        HOW TO ASSIGN EBUS        
            Define min. battery to operate (trip + empty time)
            Filter available vehicles
            Check if the available bus can handle it in the DSoC
            IF not, send bus to bus depot
            IF yes, consider bus bundle to assing trip
            Assign trip based on the best conditions
            
            All this process must be documented in a log file
        INPUTS:
        1. List of Ebus with their status and localization (E-bus method?)(requirefleetstatus)
        2. (ID/Status/location/SoC)
        3. Filter:
            1. Status:Available in PIR
            2. Location:Selected PIR(from object)(after 15min waiting (error margin)
            3. Select bus with less waiting time
            SELECT BUS
            1. Assing bus to a specific table
        '''
## Bus depot
class BusDepot:
    def __init__(self,
                 name, 
                 location_name,
                 capacity_bus,
                 capacity_chargers):
        self.name = name
        self.location_name = location_name
        self.capacity_bus = capacity_bus
        self.capacity_chargers = capacity_chargers
        self.chargers = []
        self.bus_fleet = []
            
    def add_charger(self, charger):
        # Add chargers until reach max amount of chargers
        if(len(self.chargers)< self.capacity_chargers):
            self.chargers.append(charger)
            log = "Charged added successfully"
        else:
            log = "Total amount of chargers reached, charger not added"
        print(log)
        
    def add_bus(self, eBus):
        # Add buses until reach max amount of ebus
        if(len(self.bus_fleet)<self.capacity_bus):
            self.bus_fleet.append(eBus)
            log = "EBus added successfully"
        else:
            log = "Total amount of EBus reached, EBus not added"
        print(log)            
    
        
## Chargers
class Charger:
    
    def __init__(self,
                 brand,
                 model,
                 n_dispensers,
                 total_power,
                 single_power,
                double_power):
        self.brand = brand
        self.model = model
        self.n_dispensers = n_dispensers
    

# Bus Object example



bus1 = eBus('Sunwin','EVB8m',2023,250,True, 0.9,0.75, 1,1,0)
bus2 = eBus('Yutong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0)
bus3 = eBus('Zhongtong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0)

for item in eBus.fleet:
    item.assignStatus("Parked")
    
for item in eBus.fleet:
    item.printStatus()


#bus1.assignStatus("In route")
#bus1.runStep(1, 30)


#print(bus1.odo)

# PIR Object example

pir1 = PIR("South", ['A1'],['Depot1'], 60)


    
        
    
