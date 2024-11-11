"""### WHAT DOES THIS FILE DO? ####
    1. Pulls ~approximate~ city coordinates from "NA_Cities.csv"
    2. Identifies a current weather station in each of these cities & pulls relevant data from these stations (only current temp used right now)
    3. Determines if that city currently has daylight or not
    4. Colourmaps all weather stations current temp relative to one another, and sets daylight as 1/0 (T/F) for each weather station. 
        If 'debugging=1' this will export a CSV and .pkl file to explore the data.
    5. 



"""

# Import Meteostat library and dependencies
from datetime import datetime, timedelta, date, timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly
import os
import matplotlib as mpl
from suntime import Sun, SunTimeException

#preamble
debugging=1
Hourly.cache_dir=r'.'
WS=pd.DataFrame()
stations = Stations()
ctime_local=datetime.now()
cUTCtime=datetime.now(timezone.utc)

## ---------------------- GET LATLONG FROM CSV FILE --------------------------------
df = pd.read_csv(os.path.join(os.getcwd(),'NA_Cities.csv'))

Nrows=df.shape[0]

if debugging:
    print(df.head())
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
SUNRISE=[]
SUNSET=[]

AcceptableCutoffDate=datetime.now().date()-timedelta(days=10)

for i in range(0,Nrows):
        
    ## ---------------------- GET WEATHER STATION CLOSEST TO THESE POINTS (FROM CSV) -----------------
    loop=1
    stations = stations.nearby(df.loc[i,'LAT'],df.loc[i,'LONG'])
    stations = stations.inventory('hourly',datetime(ctime_local.year,ctime_local.month,ctime_local.day-1,0)) #inventory by what stations had reported hourly data as of hour 0 today.
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
    
    ## -------------------- GET DAYLIGHT OR NOT AT EACH STATION -----------------------------
    sun=Sun(station.latitude[0],station.longitude[0])
    
    # try/except blocks for local sunrise/sunset times so we avoid the raised exceptions for (northern in this DS) places
    # which do not have sunrise/sunset every day all year 'round.
    try: 
        SR=sun.get_local_sunrise_time(time_zone=timezone.utc)
    except:
        SR=datetime(2024,1,1,1,1,1,tzinfo=timezone.utc)
    
    try:
        SS=sun.get_local_sunset_time(time_zone=timezone.utc)
    except:
        SS=datetime(2024,1,1,0,0,0,tzinfo=timezone.utc)
    
    # # This functionality moved to rpi local.
    # if SR<=cUTCtime>=SS:
    #     dayli=1
    # else:
    #     dayli=0
    
    SUNRISE.append(SR)
    SUNSET.append(SS)
    
    if debugging:
        print('current lists')
        print(ICAO,LATS,LONGS,CTEMP,SNOW)

## -------------------------------------- COLORMAPPING HERE -------------------------------------------------
clrmapped=mpl.colormaps['jet']
norm=mpl.colors.Normalize(min(CTEMP),max(CTEMP))
colors=clrmapped(norm(CTEMP))

## -------------------------------------- ADD DATA TO DF ---------------------------------------------------
    
add2DF={'ICAO':ICAO,'Name':NAME,'Country':COUNTRY,'Region':REGION,'Latitude':LATS,'Longitude':LONGS,'Ctemp':CTEMP,'Snow':SNOW,'RGBA':colors.tolist(),'Sunrise':SUNRISE,'Sunset':SUNSET}

keepers=pd.DataFrame(add2DF)

if debugging:
    keepers.to_csv(r'./Keepers_Export.csv')
    keepers.to_pickle(r'./Keepers_Export.pkl')
    #saves data to look at in csv format    

## -------------------------------------- VISUALIZE DATA LOCALLY ---------------------------------------------------
plt.scatter(keepers['Longitude'],keepers['Latitude'],c=keepers.RGBA)
plt.ylabel('LATITUDE')
plt.xlabel('LONGITUDE')
plt.title('North America Data Points - point density checker')
plt.show()

# TODO: PUSH THIS DF TO A METHOD THAT INTERFACES WITH THE ADDRESSABLE LEDs ON THE PHYSICAL MAP