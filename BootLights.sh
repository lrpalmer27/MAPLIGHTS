#!/bin/bash

sleep 5
echo 'Starting map'

# original:
# screen -S main -d -m bash -c "sudo python3 ~/Desktop/LIGHTS/RPI_main.py"

# make sure this runs on main display
export DISPLAY=:0

cd /home/lprpizero/Desktop/LIGHTS
LOGFILE='/home/lprpizero/Desktop/LIGHTS/logs/logfile.txt'

echo 'BootWallLights.sh opened' >> "$LOGFILE"

# start venv
# source /home/lprpizero/Desktop/LIGHTS/myvenv/bin/activate
# echo 'opened venv' >> "$LOGFILE"

# run python file
sudo python3 /home/lprpizero/Desktop/LIGHTS/RPI_main.py

echo 'opened RPI_main.py' >> "$LOGFILE"

cleanup () {
	pkill -f RPI_main.py
	sudo python3 resetLights.py
	echo 'Cleaning up program and shutting down' >> "$LOGFILE"
	sleep 20
}

trap cleanup SIGINT
trap cleanup SIGTSTP
