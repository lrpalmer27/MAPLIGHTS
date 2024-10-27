from datetime import datetime, timedelta, date, timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from meteostat import Stations, Hourly
import os
from suntime import Sun, SunTimeException

Data=pd.read_csv(os.path.join(os.getcwd(),'Keepers_Export.csv'))

print(Data.head())
print(Data.Ctemp)

## USE SUNTIME TO GET LOCAL SUNRISE/SUNSET TIME FOR EACH POINT
Long=Data.Longitude[145]
Lat=Data.Latitude[145]

sun=Sun(Lat,Long)

# try/except blocks for local sunrise/sunset times so we avoid the raised exceptions for (northern in this DS) places
# which do not have sunrise/sunset every day all year 'round.
try: 
    SR=sun.get_local_sunrise_time(time_zone=timezone.utc)
except:
    NOSUN=1
    SR=datetime(2024,1,1,1,1,1,tzinfo=timezone.utc)

try:
    SS=sun.get_local_sunset_time(time_zone=timezone.utc)
except:
    NOSUN=1
    SS=datetime(2024,1,1,0,0,0,tzinfo=timezone.utc)
    print(SS)

cUTCtime=datetime.now(timezone.utc)
print('\n\nTimeNow:',cUTCtime)
print('City:',Data.Name[145])
print('Sunrise:',SR,'\nSunburn','\nSunset:',SS,'\nRepeat!\n\n')

if SR <= cUTCtime >= SS or not NOSUN:
    Daylight=1 

ctime=datetime.now()
print('Current day with prev hour',datetime(ctime.year,ctime.month,ctime.day,ctime.hour-1))

print('end')