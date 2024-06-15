# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:42:01 2023

@author: rafle
"""
## Main modules

from datetime import timedelta
import pandas as pd
## Objects definition

## ebus



class eBus:
    ## Initial default values
    fleet = []
    
    def __init__(self, 
                 
                 # General vehicle parameters
                 
                 brand: str,            # Bus Brand
                 model: str,            # Bus model
                 year: int,             # Bus year
                 busType: str,          # Bus size (meters)
                 capacity: float,       # Bus Capacity (seated +stand)
                 busId: float,          # Bus Id defined
                 busDepot: str,         # Starting bus depot
                 
                 # Battery parameters
                 
                 capKwh: float,         # Battery capacity in Kilowatts hour 
                 soc: float,            # SoC in kWh
                 #socpe: float,          # Soc in percentage                 
                 
                 # Consumption parameters
                 
                 acON: bool,            # Bool (is using AC?)
                 consAC: float,         # Reference consumption using AC
                 consNoAC: float,       # Reference consumption not using AC
                 speedFact: list,        # Consumption speed modifier based on graphics
                 
                 #Basic operation 
                 
                 odo: float,            # Odometer
                 maxChargeDay: float,    # Max percentage of battery in day
                 maxChargeNight: float,  # Max percentage of battery in night
                 minCharge: float,       # Min percentage of battery allowed
                 battDeg: float         # Percentage of battery degradation
                 
                 ):
        # Example
        '''
        
        bus1 = eBus('Sunwin','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus1")
        
        '''
        ## Assign self initial parameters
        
        self.brand = brand
        self.model = model
        self.year = year
        self.busType = busType
        self.capacity = capacity
        self.busId = busId
        self.busDepot = busDepot
        
        self.capKwh = capKwh
        self.soc = soc
        
        self.ac = acON
        self.consAC = consAC
        self.consNoAC = consNoAC
        self.speedFact = speedFact

        self.odo = odo
        self.emptyOdo = 0
        self.routeOdo = 0
        self.maxChargeDay = maxChargeDay
        self.maxChargeNight = maxChargeNight
        self.minCharge = minCharge
        self.battDeg = battDeg
        
        # Default parameters
        
        self.routePosit = 0
        self.tripscounter = 0
        self.routeLengt = 999999
        ## Actions
        eBus.fleet.append(self)
        
    
    def setInitialBattery(self,charge):
        # Define battery based on degradation
        self.capKwh = self.capKwh*(1-self.battDeg)
        print("Max capacity of a degraded battery set in "+ str(self.capKwh))
        self.batEneKwh = min(self.capKwh, charge) 
        self.soc = self.batEneKwh/self.capKwh
        self.socpe = self.batEneKwh/self.capKwh*100
        
        print("The battery has been defined as {} kWh, {} % of the battery".format(str(self.batEneKwh),
                                                                                   str(self.socpe)))             

    def assignStatus(self, status):
        self.status = status
    def restartRoutePosit (self):
        self.routePosit = 0
    def innitializeRoute(self, routeName, routeLen, routeSpeed, emptyLengt):
        ## Prueba con ruta standar
        '''
        freq = 5 # 5 minutos
        routeLen = 22
        routeSpe = 17
        cycleTime = (routeLen/routeSpe)*60
        routeName = "Imaginary route"
        '''
        ##
        self.routeName = routeName
        self.routeLengt = routeLen 
        self.routePosit = 0
        self.routeSpeed = routeSpeed
        self.emptyLengt = emptyLengt
        
        
    def setBusId (self, identifier):
        self.identifier = identifier
    def setInitialLocation (self, placeType, place):
        self.placeType = placeType
        self.place = place
        
    def runStep(self, step, speed, simStep):
       
        currentStatus = self.status
        energy = step*speed
        #print(energy)
                              
        '''
        
        Bus activity based in the status:
        Status
        - Parked = No displacement, no consumption, no charging, ready to be assigned
        - Charging = No displacement, no consumption, charging
        - Charged = ready for a new service
        - GoingPIR = Circulating out of the route, discharging
        - GoingBD  = Circulating out of the route, discharging
        - InRoute = Circulating in route, discharging
        - Hold = Stopped in bus depot discharged
        Check status
        
        '''
        ## Transit
        if (self.status == "InTransit"):
            ## Move the bus around the emtpy length
            ## Once the empty lenght has been reached, it pass to InRoute
            self.odo = self.odo + self.routeSpeed*(step/60)
            self.routePosit = min(self.routePosit + self.routeSpeed*(step/60), self.emptyLengt)
            if (self.routePosit == self.emptyLengt):
                self.status = "AvailableInPIR"
                self.routePosit = 0
                
            
            
        if (self.status == "InRoute"):
            # In route should 1. Check SoC
            # Adjust SoC
            # Update position
            # Stop if SoC <+ 10%
            #print(self.busId + self.status)
            self.soc = self.soc - (self.routeSpeed*(step/60))*self.consAC
            self.odo = self.odo + self.routeSpeed*(step/60)
            # Update route
            self.routePosit = min(self.routePosit + self.routeSpeed*(step/60), self.routeLengt)
            
            #Check if bus has arrived route end, assign as available if it has enough battery, if not, send to BUs depot to charge
            if(self.routePosit == self.routeLengt):
                
                self.routePosit = 0
                self.tripscounter = self.tripscounter + 1
                
                if(self.soc > (250*.1)+(22*.9)):
                    self.status = "AvailableInPIR"
                else:
                    self.status = 'ReturnToDepot'
                    self.routePosit = 0
        
        ### If returning to Depot, discharge and count
        
        if (self.status == 'ReturnToDepot'):
            self.soc = self.soc - (self.routeSpeed*(step/60))*self.consAC
            self.odo = self.odo + self.routeSpeed*(step/60)
            self.routePosit = min(self.routePosit + self.routeSpeed*(step/60), self.emptyLengt)
            if (self.routePosit == self.emptyLengt):
                self.status = "Parked"
                self.routePosit = 0
            
                
                
                
                

                
                #log = s.printAndCompileMsg(self.busId + "has arrived to end of the route,at sim step" + str(simStep) +" send to parking",log)

            
            

        elif(self.status == "Charging"):
            maxCharge = self.capacity
            charge = self.soc + (120*(step/60)) ##120kwh power, change to a variable soon (from charger)
            
            self.soc = min(maxCharge, charge)
            if (self.soc == maxCharge):
                self.status = "Parked"
                self.routePosit = 0
                
                
            

            
        
        
        

        
    
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

## Example from environment bus

busRepo = pd.read_csv('Environment/Ebus_specifications.csv')

busModel1 = busRepo.iloc[0]

fleetExample = []

fleetNames = ['Bus1', 'Bus2', 'Bus3', 'Bus4','Bus5']

for bus in fleetNames:
    bus = eBus(busModel1.Brand,
               busModel1.Model,
               busModel1.Year,
               busModel1.Type,
               busModel1.CapacityPax,
               bus,
               "South",
               busModel1.batteryCap,
               busModel1.SoC,
               busModel1.acON,
               busModel1.consAC,
               busModel1.consNoAC,
               busModel1.speedfacts,
               busModel1.odo,
               busModel1.maxChargeDay,
               busModel1.maxChargeNight,
               busModel1.minSoC,
               busModel1.battDeg
               )
    fleetExample.append(bus)

for i in range(0,len(fleetExample)):
    fleetExample[i].setInitialBattery(190)
    fleetExample[i].innitializeRoute('TestRoute', 35, 13, 7)
    
'''
bus1 = eBus('Sunwin','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus1")
bus2 = eBus('Yutong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus2")
bus3 = eBus('Zhongtong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus3")
'''
for item in eBus.fleet:
    item.assignStatus("Parked")
    
for item in eBus.fleet:
    item.printStatus()

print(fleetExample[0].soc)
#bus1.assignStatus("In route")
#bus1.runStep(1, 30)


#print(bus1.odo)

# PIR Object example

pir1 = PIR("South", ['A1'],['Depot1'], 60)


    
        
    
