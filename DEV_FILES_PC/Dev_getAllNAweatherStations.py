# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
from datetime import timedelta

# Get nearby weather stations
stations = Stations()
stations = stations.nearby(35.4167, -97.3833) #dead center canada to use as starting point
station = stations.fetch(1)

print(station)

ctime_local=datetime.now()
hourlyData=Hourly(station,ctime_local-timedelta(hours=1),ctime_local)
Hrly=hourlyData.fetch()

print(Hrly)

