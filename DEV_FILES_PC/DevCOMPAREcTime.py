from datetime import datetime, timedelta, date, timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from meteostat import Stations, Hourly
import os
from suntime import Sun, SunTimeException

Data=pd.read_pickle(os.path.join(os.getcwd(),'./cDATA.pkl'))
print(Data.head)


cUTCtime=datetime.now(timezone.utc)
cCentralTime=datetime.now(timezone.utc)-timedelta(hours=6)
print(cCentralTime)


#initialize time variables
startingTime=datetime.now(timezone.utc)
cUTCtime=datetime.now(timezone.utc)

while True: # regenerate data every 15 mins...? TODO: fix this.
    
    # # Import the current data pickle file.
    Data=pd.read_pickle(os.path.join(os.getcwd(),'./cDATA.pkl'))

    # # Get sunrise/sunset time in Dallas (approx build location)
    sun=Sun(32.7767,-96.7970)
    BuildLocationSunrise=sun.get_local_sunrise_time(time_zone=timezone.utc)
    BuildLocationSunset=sun.get_local_sunset_time(time_zone=timezone.utc)
        
    # # Loop this every few seconds I guess? # TODO make this a function that loops until the data needs to be regenerated.
    # # Check current time.
    cUTCtime=datetime.now(timezone.utc)
    if BuildLocationSunrise<=cUTCtime>=BuildLocationSunset:
        localDaylight=1
    else:
        localDaylight=0.75 #Use this to modify how much less bright it gets.
        
    # # Go though each row in pkl df and determine if it is local daylight or not. 
    for rowN in range(0,len(Data.Sunrise)):
        if Data.Sunrise[rowN]<=cUTCtime>=Data.Sunset[rowN]:
            #daylight in that locaton
            stationdayli=1
        else:
            #not daylight in that locaton. Use this to modify how much less bright it gets.
            stationdayli=0.75
            
        #get the 0-1 range rgb value in pkl df. *255 to swith to 0-255 ish.
        print(Data.RGBA[rowN])    
        ConsiderateRGBA=(pd.Series(Data.RGBA[rowN])*255*stationdayli*localDaylight).tolist()
        print(ConsiderateRGBA)
        print(ConsiderateRGBA[0])