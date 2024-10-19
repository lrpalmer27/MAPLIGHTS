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
Long=Data.Longitude[0]
Lat=Data.Latitude[0]

sun=Sun(Lat,Long)

SR=sun.get_local_sunrise_time(time_zone=timezone.utc)
SS=sun.get_local_sunset_time(time_zone=timezone.utc)

cUTCtime=datetime.now(timezone.utc)
print('\n\nTimeNow:',cUTCtime)
print('City:',Data.Name[0])
print('Sunrise:',SR,'\nSunburn','\nSunset:',SS,'\nRepeat!\n\n')

if SR <= cUTCtime >= SS:
    Daylight=1 

ctime=datetime.now()
print('Current day with prev hour',datetime(ctime.year,ctime.month,ctime.day,ctime.hour-1))

print('end')