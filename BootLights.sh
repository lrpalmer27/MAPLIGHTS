#!/bin/bash

sleep 5
echo 'Starting map'

# original:
# screen -S main -d -m bash -c "sudo python3 ~/Desktop/LIGHTS/RPI_main.py"

# make sure this runs on main display
export DISPLAY=:0

cd /home/lprpizero/Desktop/LIGHTS
LOGFILE='/home/lprpizero/Desktop/LIGHTS/logs/logfile.txt'

sudo python resetLights.py 
echo 'Bootup -> clear Lights' >> "$LOGFILE"

# run python file
sudo python3 /home/lprpizero/Desktop/LIGHTS/RPI_main.py 

echo 'opened RPI_main.py' >> "$LOGFILE"

killNcleanup () {
	echo "Stopping script. /n Cleaning up..."
	sudo pkill -f RPI_main.py
	sudo python resetLights.py 
	sleep 3
	echo 'cleaned up, shutting down' >> "$LOGFILE"

}

trap killNcleanup SIGINT
trap killNcleanup SIGTSTP
