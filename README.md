# LIGHT UP MAP PROJECT
This project is based on this project, which I found on Facebook. They are commercially available here: https://metarmaps.com/. I wanted to add Canada, and a select few cities that are meaningful to me. I want to learn to solder and properly implement a reliable RPI based sym to run the final product.

<img src="Assets/Inspo.png" alt="drawing" width="200"/>

## Basis
This project is based on the Metostat library of maintained weather data across the globe.

Check out Metostat:
    https://meteostat.net/en/

Starting set of north american city coordinates courtesy of: https://www.infoplease.com/us/geography/latitude-and-longitude-us-and-canadian-cities

Futher edits and functionality beyond these two sources are built by yours truly. 

## Version Compatibility
I am running this on a Raspberry Pi Zero running Bullseye and Python 3.9.2 with the following dependencies:

    rpi_ws281x
    adafruit-circuitpython-neopixel
    meteostat
    suntime

It should be noted that in addition to these requirements, these items needed to be run

    sudo python3 -m pip install --force-reinstall adafruit-blinka
    sudo apt-get install python3-pandas

 Plus: 

    "raspi-config" & enable GPIO pins

For testing I am running these requirements on PC with Python 3.9.2: 

    matplotlib==3.9.2
    meteostat==1.6.8
    suntime==1.3.2

Additional requirements & versions can be found in the "requirements.txt" file.

## Current State
Ability to pull weather stations from a list of starting points (city coordinates) (which has been updated to reduce iterations to find them in future reps.) and plot them on a matplotlib scatter plot. The weather station coordinates are also exported to .csv. CSV coords can easily be imported to google earth pro and viewed to validate point density (as shown below).

<img src="Assets/PLOT_OF_SELECTED.png" width=300> <img src="Assets/PLOT_OF_SELECTED_OVERLAID.png" width=200>

Functionality has been added to grab current temperatures at each of the selected weather stations, and colour map them between the High/Low temperatures in the range. RGB values are extracted to a DF to be applied to the LEDs in future works. For troubleshooting the RGB colours are plotted on a Matplotlib plot.

<img src='Assets/NA_ColourMapped_stations.png' width=400>

A base map has also been created and printed, using QGIS (https://www.qgis.org/) software, along with shapefiles of Canada, and the United States exported from fed resources (linked in the future). Basemap seen below.

<img src='Assets/BlackWhiteBasemap.png' width=400>

Added the ability to check if each station is in local daylight. Plotting on Matplotlib as semi-transparent.

<img src='Assets/NA_ColourMapped_stations_wDaylight.png' width =400>

Plotting actual weather station coordinates on top of map that was actually printed using QGIS, we can thin out the datapoints such that the actual build looks cleaner and less crowded. This is the current state: 

<img src='Assets/DATAPOINT_DENSITY.png' width=400>

Map as shown above has been printed, and assembled onto a POC frame, consisting of an MDF backboard, and two pine upper/lower boarders to squeeze the map poster in place. 
Ø 1/4" holes are drilled, for the neopixels, all ~130 neopixels are hot glued onto the back of the MDF board. 3x 22AWG solid core wires are soldered onto the first neopixel, with 3x wires extending from each neopixel to the subsequent (6x leads on each neopixel).

A 5V 45W laptop charger is used to power the system. According to neopixel best practices a small resistor is equipped to reduce noise in the data line, and a small capacitor is used to control power surges on the 5V line.

The below picture shows the build's current state: 

<img src='Assets/PhysicalMapBuild_example01.jpg' width=400>

A digital timelapse of the project is made, and will be used to later contrast a timelapse of the physical project itself. 
"GenDigitalMap.py" is used to generate the timelapse data across a date range, and resolution specified. 
"MapDemoVidMaker.py" combined the timelapse images into a video.

An example of the digital version at a midpoint, and the timelapse mp4:

<img src='Assets/TimelapseDataExample.png' width=400>

<video width="400" controls>
    <source src="AllDayTimelapse.mp4" type="video/mp4">
</video>

## Future Works
Currently pending, is to re-order the "NA_Cities.csv" file to match the sequence that the neopixels are actually soldered together. I found it easier to decide the actual sequence during the soldering process rather than trying to follow a mapped sequence.

The "RPIDEV_FILES/debug_elec.py" file allows one light at a time to be turned on, and reports the index number. So, to re-order the NA_cities.csv file will simply be a matter of using the debug file and matching up the geographical location.

A few dots shown in the digital examples are omitted for the acutal build because of physcial B-side space constraints. So the omitted dots will be removed during this calibration phase too.
    
