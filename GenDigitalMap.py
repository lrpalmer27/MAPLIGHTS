""" The purpose of this file is to generate a digital version of the 'map', to show us what it is supposed to do, when electical issues are fully debugged.

Objective: 
Iterate over a set time period of ~1 day, generating and saving a plot of the map, at a set time interval
"""

import time
import os
from datetime import datetime, timedelta, date, timezone
import argparse
import pandas as pd
import numpy as np
from DATAGENERATOR import GENERATEDATA
from suntime import Sun, SunTimeException
import matplotlib.pyplot as plt
import matplotlib as mpl

debugging=0

if __name__=="__main__":
    
    if True: #objective of this statement is to make a timelapse of the sun rising across NA (finer resolution, less time)
        TimePeriodStart=datetime(2024,12,19,11,0,0)
        samples2gen=240
        TimeLength=timedelta(hours=14)
    if False: #objective of this statement is to make a timelapse of the tempertures across the whole day (coarser resolution, more time)
        TimePeriodStart=datetime(2024,12,19,0,0,0)
        samples2gen=int(24*60/15)
        TimeLength=timedelta(days=1)
        
    timespace=np.linspace(TimePeriodStart,TimePeriodStart+TimeLength,samples2gen)
    
    # Open time loop ---
    for i in timespace:
        ConsiderateRGBA=[] #clear list at each time step.
        i=datetime.replace(i,second=0,microsecond=0)
        print(i)
        ctime_local=i
        cUTCtime=datetime.replace(i,tzinfo=timezone.utc)
        print(cUTCtime,ctime_local)
        
        GENERATEDATA(debugging=0,times=[ctime_local,cUTCtime])
        
        # # Import the current data pickle file.
        Data=pd.read_pickle(os.path.join(os.getcwd(),'cDATA.pkl'))
        
        # # initialize time variables
        # startingTime=datetime.now(timezone.utc)
        # cUTCtime=datetime.now(timezone.utc)

        # # Get sunrise/sunset time in Dallas (approx build location)
        sun=Sun(32.7767,-96.7970) #dallas coords
        BuildLocationSunrise=sun.get_local_sunrise_time(ctime_local,time_zone=timezone.utc)
        BuildLocationSunset=sun.get_local_sunset_time(ctime_local,time_zone=timezone.utc)
        
        if BuildLocationSunrise<=cUTCtime>=BuildLocationSunset:
            localDaylight=1
        else:
            # localDaylight=0.8 #Use this to modify how much less bright it gets.
            localDaylight=1 # see note below
            """ dont have this feature enabled for digital POC, it looks funny and isnt intuitively
                understood when looking at the video from an alternate geographical location in timelapse mode """
            
        # # Go though each row in pkl df and determine colour considerate of local and station sunset times. 
        for rowN in range(0,len(Data.Sunrise)):               
            if Data.Sunrise[rowN]<=cUTCtime<=Data.Sunset[rowN]:
                #daylight in that locaton
                stationdayli=1
            else:
                #not daylight in that locaton. Use this to modify how much less bright it gets.
                stationdayli=0.6
           
            #get the 0-1 range rgb value in pkl df and convert to a brightness considerate.    
            cRGBA=(pd.Series(Data.RGBA[rowN])*stationdayli*localDaylight).tolist()
            ConsiderateRGBA.append(cRGBA)
            
        plt.figure('Digital Map Example - looping')
        plt.scatter(Data.Longitude,Data.Latitude,c=ConsiderateRGBA)
        plt.title(f'Digital Map Example\nTime (UTC): {i}')
        plt.ylabel('Latitude')
        plt.xlabel('Longitude')
        
        if debugging:
            plt.show()
        else:
            name=f'{i}'
            name=name.replace(':',' ')
            print(name) #for status checking
            
            plt.savefig(f'.AllDigitalMapShots/{name}.png', bbox_inches='tight',dpi=600)