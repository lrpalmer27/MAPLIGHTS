import time
import os
from datetime import datetime, timedelta, date, timezone
from pytz import timezone as ptztz
# from rpi_ws281x import *
import argparse
import pandas as pd
from suntime import Sun, SunTimeException

def ConvertStrTime2dt(stringDT,currentTime):
    DT_format=datetime.strptime(stringDT,'%H:%M')
    DT_format=DT_format.replace(year=currentTime.year,month=currentTime.month,day=currentTime.day,tzinfo=LocalTimeZone)

    return DT_format


LocalTimeZone = ptztz('America/Los_Angeles')
cUTCtime=datetime.now(LocalTimeZone)
currentTime=cUTCtime


df = pd.read_csv(os.path.join(os.getcwd(),'OperatingTimes.csv'))

if currentTime.weekday() < 5: 
    ontime_str=df.loc[0,'ON']
    offtime_str=df.loc[0,'OFF']
    ontime1_str=df.loc[1,'ON']
    offtime1_str=df.loc[1,'OFF']
    
    if (currentTime > ConvertStrTime2dt(ontime_str,currentTime) and currentTime < ConvertStrTime2dt(offtime_str,currentTime)) or (currentTime > ConvertStrTime2dt(ontime1_str,currentTime) and currentTime < ConvertStrTime2dt(offtime1_str,currentTime)):
        #  this means it should be ON
        Sleep = 0
    
    else:
        # How much sleep do we need?
        if currentTime > ConvertStrTime2dt(ontime1_str,currentTime):
            # sleep all night!
            ONTIME=ConvertStrTime2dt(ontime_str,currentTime)
            ON_TIME_TMRW = ONTIME.replace(day=((currentTime+timedelta(days=1)).day))
            SleepTime = (ON_TIME_TMRW-currentTime).seconds 
        
        elif currentTime > ConvertStrTime2dt(offtime_str,currentTime) and currentTime < ConvertStrTime2dt(ontime1_str,currentTime):
            #  sleep until this afternoon!
            ONTIME = ConvertStrTime2dt(ontime1_str,currentTime)
            SleepTime=(ONTIME-currentTime).seconds

if currentTime.weekday() >= 5:
    ontime_str=df.loc[0,'ON']
    offtime_str=df.loc[0,'OFF']
    
    if currentTime > ConvertStrTime2dt(ontime_str,currentTime) and currentTime < ConvertStrTime2dt(offtime_str,currentTime):
        # this means it should be ON!
        Sleep = 0 
    
    else: 
        ONTIME=ConvertStrTime2dt(ontime_str,currentTime)
        ON_TIME_TMRW = ONTIME.replace(day=((currentTime+timedelta(days=1)).day))
        SleepTime = (ON_TIME_TMRW-currentTime).seconds




