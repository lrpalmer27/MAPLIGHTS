from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from meteostat import Stations, Hourly
import os

Data=pd.read_pickle(os.path.join(os.getcwd(),'./cData.pkl'))

plt.figure('NA default scale')
plt.scatter(Data.Longitude,Data.Latitude,c=Data.Ctemp,cmap='jet')
plt.title('North America Weather Stations - Temperature')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.colorbar()
# plt.show()

# ## ---------------- DEV COLOR MAPPING HERE ---------------------

# #mpl.colormaps not available on the useable version of mpl on rpi

# # clrmapped=mpl.colormaps['jet'] # for mpl 3.9.2
# clrmapped=mpl.colors.Colormap['jet'] # for mpl 3.3.4
# norm=mpl.colors.Normalize(Data.Ctemp.min(),Data.Ctemp.max())
# colors=clrmapped(norm(Data.Ctemp))
# # print(colors)

# plt.figure('NA custom cmap scale')
# plt.scatter(Data.Longitude,Data.Latitude,c=colors)
# plt.title('North America Weather Stations - Temperature, custom cmap')
# plt.ylabel('Latitude')
# plt.xlabel('Longitude')
# plt.colorbar()
# plt.show()

## ---------------- plotted straight from CSV -----------------------
RGBA=Data.RGBA
Daylight=Data.Daylight
NEWRGBA=[]
# print(Data.head())
# # print(Daylight)
# print(type(Data.RGBA[0]))

for rowN in range(0,len(Daylight)):
    print(rowN,RGBA[rowN])
    print(type(RGBA[rowN]))
    if not Daylight[rowN]:
        nColour=[RGBA[rowN][0],RGBA[rowN][1],RGBA[rowN][2],0.25]
        print(nColour)
        NEWRGBA.append(nColour)
    else: 
        NEWRGBA.append(RGBA[rowN])

plt.figure('DatafromCSV - includes daylight/notdaylight')
plt.scatter(Data.Longitude,Data.Latitude,c=NEWRGBA)
plt.title('North America Weather Stations - Temp +  Daylight (Dev)')
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.colorbar()


plt.show()

print('end')