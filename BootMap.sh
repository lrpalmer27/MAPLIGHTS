#!/bin/bash

echo 'Start'
sleep 10
screen -S main -d -m bash -c "sudo python3 ~/Desktop/LIGHTS/RPI_main.py"
echo 'Started map'
