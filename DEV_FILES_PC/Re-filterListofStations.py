# Import Meteostat library and dependencies
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
from datetime import timedelta
import os 
from pytz import timezone as ptztz

LocalTimeZone = ptztz('America/Los_Angeles')
ctime_local=datetime.now()
AcceptableCutoffDate=ctime_local.date()-timedelta(days=10)

df = pd.read_csv(os.path.join(os.getcwd(),'NA_cities.csv'))
Nrows=df.shape[0]

stations = Stations()

for i in range(0,Nrows):
    loopN=1
    
    stations = stations.nearby(df.loc[i,'LAT'],df.loc[i,'LONG'])
    print('coords',df.loc[i,'LAT'],df.loc[i,'LONG'])
    station=stations.fetch(1)
    stations = stations.inventory('hourly',datetime.replace(ctime_local,hour=0,minute=0,second=0,microsecond=0)) #inventory by what stations had reported hourly data as of hour 0 today.
    station = stations.fetch(1)
    
    print(station.iloc[0])
    
    while station['hourly_end'].iloc[-1].date() < (AcceptableCutoffDate):
        loop+=1
        print("new loop", station)
    