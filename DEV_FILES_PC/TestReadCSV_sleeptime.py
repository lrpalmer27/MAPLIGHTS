import os
from datetime import datetime, time, timedelta
import time
import pandas as pd

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

ON_TIME_TMRW=ON_TIME.replace(day=((datetime.now()+timedelta(days=1)).day))
SleepTime = ON_TIME-datetime.now()

print(SleepTime.seconds)

time.sleep(0)

print("none")