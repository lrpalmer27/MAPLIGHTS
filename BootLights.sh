#!/bin/bash

sleep 5
echo 'Starting map'

# make sure this runs on main display
export DISPLAY=:0

cd /home/lprpizero/Desktop/LIGHTS
LOGFILE='/home/lprpizero/Desktop/LIGHTS/logs/logfile.txt'

# open scheduled reboot tool - this is a brute force way to deal with weird meteostat data pulling problem
lxterminal -e /home/lprpizero/Desktop/LIGHTS/rpiScheduledReboots.sh &
echo "rpiScheduledReboots.sh opened @ $(date "+%r")" | tee -a "$LOGFILE"

# reset the lights
sudo python resetLights.py 
echo 'Bootup -> clear Lights' | tee -a "$LOGFILE"

# run the actual main file
sudo python3 /home/lprpizero/Desktop/LIGHTS/RPI_main.py 
echo 'opened RPI_main.py' | tee -a "$LOGFILE"

killNcleanup () {
	echo "Stopping script. /n Cleaning up..."
	sudo pkill -f RPI_main.py
	sudo python resetLights.py 
	sleep 3
	echo 'cleaned up, shutting down' >> "$LOGFILE"

}

trap killNcleanup SIGINT
trap killNcleanup SIGTSTP
