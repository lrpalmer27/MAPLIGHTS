#!/bin/bash

# setup same logfile 
cd /home/lprpizero/Desktop/LIGHTS
LOGFILE='/home/lprpizero/Desktop/LIGHTS/logs/logfile.txt'

echo "rpiScheduledReboots.sh running @ $(date "+%r")" >> "$LOGFILE"

# run on main display 
export DISPLAY=:0

# reboot every 6h
RESETTIME="$(date -d "+6 hour")"
echo "Rebooting in 6h, at $RESETTIME" | tee -a "$LOGFILE"

# do the actual waiting here
sleep 6h
echo "Done Sleeping. Current time $(date "+%r"). Rebooting now" | tee -a "$LOGFILE"
sudo reboot