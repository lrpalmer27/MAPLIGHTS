from suntime import Sun
from datetime import datetime, timezone

ctime_local=datetime(2024, 12, 19,0,0,0)
sun=Sun(25.7833, -80.316)
SR=sun.get_local_sunrise_time(at_date=ctime_local,time_zone=timezone.utc)
SS=sun.get_sunset_time(at_date=ctime_local,time_zone=timezone.utc)

print (SR,'\n',SS)

if SR>SS:
    print("NO")