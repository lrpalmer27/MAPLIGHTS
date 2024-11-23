
import time
import os
from datetime import datetime, timedelta, date, timezone

# initialize time variables
startingTime=datetime.now(timezone.utc)
cUTCtime=datetime.now(timezone.utc)
LOOPDURATION=0.25

print('starting time',startingTime)
print('current time',cUTCtime)
print(cUTCtime + timedelta(hours=LOOPDURATION))

while cUTCtime + timedelta(hours=LOOPDURATION) > startingTime:
    print(cUTCtime)
    input('')