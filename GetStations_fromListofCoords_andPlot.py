# Import Meteostat library and dependencies
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
import os

#preamble
debugging=1
Hourly.cache_dir=r'.'
WS=pd.DataFrame()
stations = Stations()

## ---------------------- GET LATLONG FROM CSV FILE --------------------------------
df = pd.read_csv(os.path.join(os.getcwd(),'NA_Cities.csv'))
df.head()

Nrows=df.shape[0]

if debugging:
    print(df.LONG)
    print(df.loc[1,'LONG'])
    
## --------------------- OPEN LOOP TO GRAB RELEVANT DATA FROM EACH OF THESE LOCATIONS ------------------------------
# init empty lists to append data to
ICAO=[]
LATS=[]
LONGS=[]
CTEMP=[]
SNOW=[]
COUNTRY=[]
REGION=[]
NAME=[]

AcceptableCutoffDate=datetime.now().date()-timedelta(days=10)

for i in range(0,Nrows):
        
    ## ---------------------- GET WEATHER STATION CLOSEST TO THESE POINTS (FROM CSV) -----------------
    loop=1
    stations = stations.nearby(df.loc[i,'LAT'],df.loc[i,'LONG'])
    stations = stations.inventory('hourly',datetime(2024,10,12,0))
    station = stations.fetch(loop)
    
    while station.empty: 
        loop+=1
        station=stations.fetch(loop)
    
    if debugging:
        print(station)
        varr=station['hourly_end'].iloc[0].date()
        
    while station['hourly_end'].iloc[-1].date() < (AcceptableCutoffDate):
            station=stations.fetch(loop)
            varr=station['hourly_end'].iloc[-1].date()
            loop+=1 

    ## ---------------------- GET WEATHER STATION DATA IN DICT & ADD TO DF -----------------
    data = Hourly(station,datetime.now()-timedelta(hours=1),datetime.now())
    data=data.fetch()
    
    if debugging:
        print(data)

    ICAO.append(station.icao[0])
    COUNTRY.append(station.country[0])
    REGION.append(station.region[0])
    NAME.append(station.name[0])
    LATS.append(station.latitude[0])
    LONGS.append(station.longitude[0])
    CTEMP.append(data['temp'].iloc[0])
    SNOW.append(data['snow'].iloc[0])
    
    if debugging:
        print('current lists')
        print(ICAO,LATS,LONGS,CTEMP,SNOW)
    
add2DF={'ICAO':ICAO,'Name':NAME,'Country':COUNTRY,'Region':REGION,'Latitude':LATS,'Longitude':LONGS,'Ctemp':CTEMP,'Snow':SNOW}
keepers=pd.DataFrame(add2DF)

keepers.to_csv(r'./Keepers_Export.csv')

plt.scatter(keepers['Longitude'],keepers['Latitude'],marker='x',color='r')
plt.ylabel('LATITUDE')
plt.xlabel('LONGITUDE')
plt.title('North America ONLY')
plt.show()

print('end')