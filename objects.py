# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:42:01 2023

@author: rafle
"""
## Main modules

from datetime import timedelta

## Objects definition


## ebus


## dispatcher

class eBus:
    def __init__(self, 
                 brand: str,
                 model: str,
                 year: int,
                 capacity: float,
                 ac: bool,
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

    def assignStatus(self, status):
        self.status = status
    def runStep(self, step, speed):
        
        self.odo = self.odo + speed*(step/60)
        self.soc = self.soc - (speed*(step/60))*self.consAC
        
    
# Object example

bus1 = eBus('Sunwin','EVB8m',2023,250,True, 0.9,0.75, 1,1,0)
bus1.assignStatus("In route")
#bus1.runStep(1, 30)


print(bus1.odo)

    
        
    