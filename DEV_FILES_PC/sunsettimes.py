
import time
import os
from datetime import datetime, timedelta, date, timezone
from pytz import timezone as ptztz
# from rpi_ws281x import *
import argparse
import pandas as pd
# from DATAGENERATOR import GENERATEDATA
from suntime import Sun, SunTimeException

# LocalTimeZone = ptztz('America/Los_Angeles')
LocalTimeZone =  ptztz('UTC')


sun=Sun(39.530895,-119.814972) #reno, nv coords
BuildLocationSunrise=sun.get_local_sunrise_time(at_date=datetime.now(tz=LocalTimeZone)).replace(tzinfo=LocalTimeZone)
BuildLocationSunset=sun.get_local_sunset_time(at_date=datetime.now(tz=LocalTimeZone)).replace(tzinfo=LocalTimeZone)

# BuildLocationSunrise=sun.get_local_sunrise_time(time_zone=LocalTimeZone)
# BuildLocationSunset=sun.get_local_sunset_time(time_zone=LocalTimeZone)

print(BuildLocationSunrise)
print(BuildLocationSunset)

# BuildLocationSunrise=BuildLocationSunrise.replace(tzinfo=LocalTimeZone)
# BuildLocationSunset=BuildLocationSunset.replace(tzinfo=LocalTimeZone)

cUTCtime=datetime.now(tz=LocalTimeZone)
print(cUTCtime)
if BuildLocationSunrise<=cUTCtime<=BuildLocationSunset:
    localDaylight=1
else:
    localDaylight=0.3 #Use this to modify how much less bright the whole board gets.