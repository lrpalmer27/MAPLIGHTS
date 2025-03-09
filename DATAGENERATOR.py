"""### WHAT DOES THIS FILE DO? ####
    1. Pulls ~approximate~ city coordinates from "NA_Cities.csv"
    2. Identifies a current weather station in each of these cities & pulls relevant data from these stations (only current temp used right now)
    3. Determines if that city currently has daylight or not
    4. Colourmaps all weather stations current temp relative to one another, and sets daylight as 1/0 (T/F) for each weather station. 
        If 'debugging=1' this will export a CSV and .pkl file to explore the data.
    5. 
"""

def GENERATEDATA(LocalTimeZone,debugging=0,times=[0,0]):
    """
    Debugging (optional) -  1: True - will go through some data vis steps to help understand the process
                            0: False - will be faster.
    Times (optional) -  [datetime.now(),datetime.now(timezone.utc)] - this can be used to generate data for a specific time in history. If no input, data will be generated for NOW.
    """

    # Import Meteostat library and dependencies
    from datetime import datetime, timedelta, date, timezone
    from pytz import timezone as ptztz
    import pandas as pd
    import numpy as np
    from meteostat import Stations, Hourly
    import os
    from suntime import Sun, SunTimeException
    import matplotlib as mpl

    #preamble
    # debugging=0
    Hourly.cache_dir=r'.'
    WS=pd.DataFrame()
    stations = Stations()
    
    if times == [0,0]:
        # this means no inputs are provided
        ctime_local=datetime.now()
        cUTCtime=datetime.now(LocalTimeZone)
    else:
        #this means the times variable is used to provide current times
        ctime_local=times[0]
        cUTCtime=times[1]
    

    ## ---------------------- GET LATLONG FROM CSV FILE --------------------------------
    df = pd.read_csv(os.path.join(os.getcwd(),'NA_cities.csv'))

    Nrows=df.shape[0]

    if debugging:
        print(df.head())
        print(df.LONG)
        print(df.loc[1,'LONG'])
        
    ## --------------------- OPEN LOOP TO GRAB RELEVANT DATA FROM EACH OF THESE LOCATIONS ------------------------------
    # init empty lists to append data to
    OIndex=df.ORDEREDINDEX.tolist()
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

    #this is a quick and dirty way to filter away the stations that arent being used, narrowing the list for the next step.
    AcceptableCutoffDate=ctime_local.date()-timedelta(days=10)

    for i in range(0,Nrows):
            
        ## ---------------------- GET WEATHER STATION CLOSEST TO THESE POINTS (FROM CSV) -----------------
        loop=1
        stations = stations.nearby(df.loc[i,'LAT'],df.loc[i,'LONG'])
        FilteringNewList=False
        if FilteringNewList:
            #this is good for filtering away bad stations (old ones that arent reporting anymore) from an arbitrary list of coordinates. 
            # current coordinates in the cities are based on weather station coordinates, NOT city coords, so this isnt needed every time. Causes issues sometimes at start of months/years.
            stations = stations.inventory('hourly',datetime.replace(ctime_local,hour=0,minute=0,second=0,microsecond=0)) #inventory by what stations had reported hourly data as of hour 0 today.
        station = stations.fetch(loop)
        
        if debugging:
            print('station:',station)
            print(f"loop number: {loop}")
            print("Looking for station at coordinates: (lat,long)",df.loc[i,'LAT'],df.loc[i,'LONG'])
            print("at time:",datetime.replace(ctime_local,hour=0,minute=0,second=0,microsecond=0))
            
        
        while station.empty: 
            print("empty df:\n",station.head)
            loop+=1
            station=stations.fetch(loop)
            if debugging:
                print(f'Station empty loop init, loop number: {loop}')
        
        if debugging:
            print(station)
            varr=station['hourly_end'].iloc[0].date()
            
        while station['hourly_end'].iloc[-1].date() < (AcceptableCutoffDate):
                station=stations.fetch(loop)
                varr=station['hourly_end'].iloc[-1].date()
                loop+=1 

        ## ---------------------- GET WEATHER STATION DATA IN DICT & ADD TO DF -----------------
        data = Hourly(station,ctime_local-timedelta(hours=1),ctime_local)
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
            SR=sun.get_local_sunrise_time(at_date=ctime_local,time_zone=LocalTimeZone)
        except:
            # deals with sunrise exception. Set SR to be hour 1 on Jan01 2024. This way current time can never be SR<=ctime<=SS.
            SR=datetime(2024,1,1,1,1,1,tzinfo=LocalTimeZone)
        
        try:
            SS=sun.get_local_sunset_time(at_date=ctime_local,time_zone=LocalTimeZone)
            ## Dealing with known issue of returning sunset time in previous day --- https://github.com/SatAgro/suntime/issues/13
            ## sol'n from https://stackoverflow.com/questions/72087825/issue-with-python-sun-get-sunset-time-routine
            if SR>SS:
                SS=sun.get_local_sunset_time(at_date=ctime_local+timedelta(days=1),time_zone=LocalTimeZone)
        except:
            # deals with sunrise exception. Set SS to be hour 0 on Jan01 2024. This way current time can never be SR<=ctime<=SS.
            SS=datetime(2024,1,1,0,0,0,tzinfo=LocalTimeZone)
        
        SUNRISE.append(SR)
        SUNSET.append(SS)
        
        if debugging:
            print('current lists')
            print(ICAO,LATS,LONGS,CTEMP,SNOW)

    ## -------------------------------------- COLORMAPPING HERE ------------------------------------------------
    if mpl.__version__=='3.9.2': # for local dev on pc
        cm=mpl.colormaps['jet'] 
        norm=mpl.colors.Normalize(min(CTEMP),max(CTEMP))
        colors=cm(norm(CTEMP))
        
    if mpl.__version__=='3.3.4': #for the rpi running mpl 3.3.4
        from matplotlib import cm
        cm=cm.get_cmap('jet')
        norm=mpl.colors.Normalize(min(CTEMP),max(CTEMP))
        colors=cm(norm(CTEMP))

    ## -------------------------------------- ADD DATA TO DF ---------------------------------------------------
        
    add2DF={'ORDEREDINDEX':OIndex,'ICAO':ICAO,'Name':NAME,'Country':COUNTRY,'Region':REGION,'Latitude':LATS,'Longitude':LONGS,'Ctemp':CTEMP,'Snow':SNOW,'RGBA':colors.tolist(),'Sunrise':SUNRISE,'Sunset':SUNSET}

    keepers=pd.DataFrame(add2DF)

    if debugging:
        keepers.to_csv(r'./cDATA.csv')
        #saves data to look at in csv format so its easily read.
        
    keepers.to_pickle(r'./cDATA.pkl') #always export the pkl file.

    if debugging: #just for showing data on local machine
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        ## -------------------------------------- VISUALIZE DATA LOCALLY ---------------------------------------------------
        plt.scatter(keepers['Longitude'],keepers['Latitude'],c=keepers.RGBA)
        plt.ylabel('LATITUDE')
        plt.xlabel('LONGITUDE')
        plt.title('North America Data Points - point density checker')
        
        #Add coordinate annotations on plot:
        for L in range(0,keepers.shape[0]):
            plt.annotate(f"({keepers['Longitude'][L]},{keepers['Latitude'][L]})",[keepers['Longitude'][L],keepers['Latitude'][L]],fontsize=2)
        
        plt.show()

if __name__ == '__main__':
    #if running locally
    from pytz import timezone as ptztz
    LocalTimeZone = ptztz('America/Los_Angeles')
    GENERATEDATA(LocalTimeZone, debugging=1)