# Import Meteostat library and dependencies
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly

stations = Stations()
stations = stations.nearby(48.94, -54.57) #dead center canada to use as starting point
station = stations.fetch(1)

print(station)

Hourly.cache_dir=r'C:\Users\logan\Desktop\Projects\WallMap_lights'

data = Hourly(station,datetime.now()-timedelta(hours=1),datetime.now())
data=data.fetch()

# data.plot(y=['tavg'])
# plt.show()

print(data)