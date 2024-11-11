# Import Meteostat library and dependencies
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly

stations = Stations()
stations = stations.nearby(32.4333, -104.25) #dead center canada to use as starting point
station = stations.fetch(1)

print(station)

Hourly.cache_dir=r'.'

data = Hourly(station,datetime.now()-timedelta(hours=1),datetime.now())
data=data.fetch()

# data.plot(y=['tavg'])
# plt.show()

print(data)