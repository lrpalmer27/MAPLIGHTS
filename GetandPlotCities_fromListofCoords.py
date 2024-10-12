# Import Meteostat library and dependencies
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
import os

debugging=1
Hourly.cache_dir=r'.'

## ---------------------- GET LATLONG FROM CSV FILE --------------------------------
df = pd.read_csv(os.path.join(os.getcwd(),'NA_Cities.csv'))
df.head()

Nrows=df.shape[0]

if debugging:
    print(df.LONG)

    print(df.loc[1,'LONG'])

## ---------------------- GET WEATHER STATION CLOSEST TO THESE POINTS (FROM CSV) -----------------

stations = Stations()
stations = stations.nearby(df.loc[0,'LAT'],-df.loc[0,'LONG'])
station = stations.fetch(1)

if debugging:
    print(station)

## ---------------------- GET WEATHER STATION DATA IN DICT & ADD TO DF -----------------

data = Hourly(station,datetime.now()-timedelta(hours=1),datetime.now())
data=data.fetch()

if debugging:
    print(data)

WS=pd.DataFrame()

print('end')