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
                 brand: str,            # Bus Brand
                 model: str,            # Bus model
                 year: int, #Delete?    # Bus year
                 capacity: float,       # Bus Capacity (seated +stand)
                 acON: bool,            # Bool (is using AC?)
                 consAC: float,         # Reference consumption using AC
                 consNoAC: float,       # Reference consumption not using AC
                 soc: float,            # SoC in kWh
                 socpe: float,          # Soc in percentage
                 odo: float,            # Odometer
                 busId: str             # Bus ID to identify vehicle in simulation
                 ):
        
        ## Assign self initial parameters
        
        self.brand = brand
        self.model = model
        self.year = year
        self.capacity = capacity
        self.ac = acON
        self.consAC = consAC
        self.consNoAC = consNoAC
        self.soc = capacity
        self.socpe = socpe
        self.odo = odo
        self.busId = busId
        self.routePosit = 0
        self.tripscounter = 0
        self.routeLengt = 999999
        ## Actions
        eBus.fleet.append(self)
        
    
    def setInitialBattery(self,charge):
        self.soc = min(self.capacity, (charge*self.soc))
        self.socpe = self.soc/self.capacity
        print("The battery has been defined as {} kWh, {} % of the battery".format(str(self.soc),
                                                                                   str(self.socpe)))             

    def assignStatus(self, status):
        self.status = status
    def restartRoutePosit (self):
        self.routePosit = 0
    def innitializeRoute(self):
        ## Prueba con ruta standar
        freq = 5 # 5 minutos
        routeLen = 22
        routeSpe = 17
        cycleTime = (routeLen/routeSpe)*60
        routeName = "Imaginary route"
        self.routeName = routeName
        self.routeLengt = routeLen 
        self.routePosit = 0
        self.routeSpeed = routeSpe
        self.emptyLengt = 5 
        
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



bus1 = eBus('Sunwin','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus1")
bus2 = eBus('Yutong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus2")
bus3 = eBus('Zhongtong','EVB8m',2023,250,True, 0.9,0.75, 1,1,0, "Bus3")

for item in eBus.fleet:
    item.assignStatus("Parked")
    
for item in eBus.fleet:
    item.printStatus()


#bus1.assignStatus("In route")
#bus1.runStep(1, 30)


#print(bus1.odo)

# PIR Object example

pir1 = PIR("South", ['A1'],['Depot1'], 60)


    
        
    
