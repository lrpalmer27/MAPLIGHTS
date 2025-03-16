# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
from datetime import timedelta

# Get nearby weather stations
stations = Stations()
stations = stations.nearby(43.5833, -96.75) #dead center canada to use as starting point
station = stations.fetch(2)

print(station)
print(station['latitude'])
print(station['longitude'])

ctime_local=datetime.now()
hourlyData=Hourly(station,ctime_local-timedelta(hours=1),ctime_local)
Hrly=hourlyData.fetch()

print(Hrly)

