#!/bin/bash

echo 'Starting map'
sleep 10
screen -S main -d -m bash -c "sudo python3 ~/Desktop/LIGHTS/RPI_main.py" >> /var/log/bootmapMain.log 2>&1 &
echo 'Map started sucessfully - now exiting'

exit 0
