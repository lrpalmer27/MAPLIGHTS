from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from meteostat import Stations, Hourly
import os

Data=pd.read_csv(os.path.join(os.getcwd(),'Keepers_Export.csv'))

print(Data.head())
print(Data.Ctemp)

print('Min temp in range',Data.Ctemp.   min())
print('Max temp in range',Data.Ctemp.max())

plt.figure('NA default scale')
plt.scatter(Data.Longitude,Data.Latitude,c=Data.Ctemp,cmap='jet')
plt.title('North America Weather Stations - Temperature')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.colorbar()

clrmapped=mpl.colormaps['jet']

norm=mpl.colors.Normalize(Data.Ctemp.min(),Data.Ctemp.max())

colors=clrmapped(norm(Data.Ctemp))
print(colors)

plt.figure('NA custom cmap scale')
plt.scatter(Data.Longitude,Data.Latitude,c=colors)
plt.title('North America Weather Stations - Temperature')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.colorbar()

plt.show()

print('end')