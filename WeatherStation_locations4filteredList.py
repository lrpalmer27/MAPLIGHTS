# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations

NA_Stations = pd.read_csv('C:\Users\logan\Desktop\Projects\WallMap_lights\NAStations_filtered.csv')

## Show things ---------------------------------------------------
NA_Stations.plot.scatter('longitude','latitude',marker='x',color='r')
plt.title('North America ONLY')

plt.show()