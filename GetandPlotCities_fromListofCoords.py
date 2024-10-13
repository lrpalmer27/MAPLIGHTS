# Import Meteostat library and dependencies
from datetime import datetime, timedelta, date
import pandas as pd
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
COORDS=[]
CTEMP=[]
SNOW=[]
for i in range(0,Nrows):
        
    ## ---------------------- GET WEATHER STATION CLOSEST TO THESE POINTS (FROM CSV) -----------------
    stations = stations.nearby(df.loc[i,'LAT'],-df.loc[i,'LONG'])
    station = stations.fetch(1)
    
    if debugging:
        print(station)
        
    loop=2
    while station['hourly_end'].iloc[-1].date() < (datetime.now().date()-timedelta(days=60)):
            # print(station['hourly_end'].iloc[-1].date())
            station=stations.fetch(loop)
            # print(station['hourly_end'].iloc[-1].date())
            loop+=1 

    ## ---------------------- GET WEATHER STATION DATA IN DICT & ADD TO DF -----------------
    data = Hourly(station,datetime.now()-timedelta(hours=1),datetime.now())
    data=data.fetch()
    
    if debugging:
        print(data)

    ICAO.append(station.icao[0])
    COORDS.append([station.latitude[0],station.longitude[0]])
    CTEMP.append(data['temp'].iloc[0])
    SNOW.append(data['snow'].iloc[0])
    
    if debugging:
        print('current lists')
        print(ICAO,COORDS,CTEMP,SNOW)
    


# add2DF={'ICAO':station.icao[0],'Coords':[station.latitude[0],station.longitude[0]],'Ctemp':data['temp'].iloc[0],'Snow':data['snow'].iloc[0]}
print('end')