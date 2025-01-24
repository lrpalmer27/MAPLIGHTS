import os
from datetime import datetime, time, timedelta, timezone
from pytz import timezone as ptztz
import time
import pandas as pd

currentTime=datetime.now(ptztz('America/Chicago'))

#read shutdown times
df = pd.read_csv(os.path.join(os.getcwd(),'OperatingTimes.csv'))
ontime_str=df.loc[0,'ON']
offtime_str=df.loc[0,'OFF']

#convert ontime and offtime strings into datetime formats
ON_TIME=datetime.strptime(ontime_str,'%H:%M')
ON_TIME=ON_TIME.replace(year=currentTime.year,month=currentTime.month,day=currentTime.day,tzinfo=ptztz('America/Chicago'))

OFF_TIME=datetime.strptime(offtime_str,'%H:%M')
OFF_TIME=OFF_TIME.replace(year=currentTime.year,month=currentTime.month,day=currentTime.day,tzinfo=ptztz('America/Chicago'))

#compare current time to shutdown times
if currentTime>ON_TIME and currentTime<OFF_TIME:
    #this means the map should be operational
    SleepTime=0
else: 
    #if the above are not satisfied, then we need to sleep the machine until sunrise the upcoming morning
    ON_TIME_TMRW=ON_TIME.replace(day=((currentTime+timedelta(days=1)).day))
    SleepTime = (ON_TIME_TMRW-currentTime).seconds

print(SleepTime)
print(currentTime)
print(ON_TIME)
print(OFF_TIME)

"""
df = pd.read_csv(os.path.join(os.getcwd(),'OperatingTimes.csv'))

print(df)

ontime_str=df.loc[0,'ON']
offtime_str=df.loc[0,'OFF']

#collect current data
year=datetime.now().year
month=datetime.now().month
day=datetime.now().day

ON_TIME=datetime.strptime(ontime_str,'%H:%M')
ON_TIME=ON_TIME.replace(year=year,month=month,day=day)
print("ontime",ON_TIME)

OFF_TIME=datetime.strptime(offtime_str,'%H:%M')
OFF_TIME=OFF_TIME.replace(year=year,month=month,day=day)
print("off time",OFF_TIME)

print(datetime.now()<OFF_TIME)

print(datetime.now()+timedelta(days=1))

print(((datetime.now()+timedelta(days=1)).day))

ON_TIME_TMRW=ON_TIME.replace(day=((datetime.now()+timedelta(days=1)).day),tzinfo=timezone.utc)
SleepTime = ON_TIME_TMRW-datetime.now(timezone.utc)

print(SleepTime.seconds)

time.sleep(0)

print("none")

"""