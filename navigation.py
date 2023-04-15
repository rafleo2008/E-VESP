# -*- coding: utf-8 -*-
"""
Segment Polylines by distance

@author: rafle
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import LineString


line = gpd.GeoSeries(LineString([(-74.03253077542105, 4.719830647616595),
                                 (-74.03273632649649, 4.712920728860805),
                                 (-74.04294788946703, 4.716330843893897)]),
                     crs = 'EPSG:4326')
line.explore().save("Example.html")

line = line.to_crs('EPSG:3116')
print(line.head())
                                  
residuo = 0 



routeLength = line.geometry.iloc[0].length
print("Areas")
print(routeLength)


mycoords = list(line.iloc[0].coords)



points = gpd.GeoSeries()
distances = []

for distance_along in np.arange(0, routeLength, int(100)):
    point = line.interpolate(distance_along)
    distance = int(line.project(point))
    points = points.append(point)
    distances.append(distance)
    
    

print("Checkintermediatecoords")
#print(coords)


points.crs = 'EPSG:3116'

gdfpoints = gpd.GeoDataFrame(geometry = points)
gdfpoints["Distance_along"] = distances
gdfpoints["Route"] = "Route AA"
gdfpoints["Direction"] = "North - South" 
gdfpoints.explore().save("Example2.html")
#print(points)
print(distances)

