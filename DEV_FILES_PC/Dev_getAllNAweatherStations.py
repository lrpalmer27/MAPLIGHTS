# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
from datetime import timedelta
from pytz import timezone as ptztz


Hourly.cache_dir=r'.'
# Get nearby weather stations
stations = Stations()
# stations = stations.nearby(39.5349, -119.7527)
stations = stations.nearby(27.9667, -82.5333)
# stations = stations.inventory('hourly',datetime(2025,3,17))
station = stations.fetch(2)

print('Station \n',station)
print('station icao',station.iloc[-1,4])

# station = '72488'

# hourlyData=Hourly(station.iloc[0,3],datetime(2025,3,17,12),datetime(2025,3,17,20))
hourlyData=Hourly('72211',datetime(2025,6,15,7),datetime(2025,6,15,7))
Hrly=hourlyData.fetch()

print('hrly.shape',Hrly.shape)
print('Hourly data',Hrly)


