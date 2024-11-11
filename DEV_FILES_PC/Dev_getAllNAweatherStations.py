# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations

# Get nearby weather stations
stations = Stations()
stations = stations.nearby(53.014783, -96.152344) #dead center canada to use as starting point
station = stations.fetch(5000)

## finds and drops non-north american weatherstations ----------------
Canadian=station.index[station['country'] == 'CA'].tolist()
American=station.index[station['country'] == 'US'].tolist()
NorthAmerican=Canadian+American

NA_Stations=station.loc[NorthAmerican]

# NA_Stations.to_csv("NAStations.csv") #debugging

## Show things ---------------------------------------------------
NA_Stations.plot.scatter('longitude','latitude',marker='x',color='r')
plt.title('North America ONLY')

plt.show()