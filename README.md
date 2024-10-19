# LIGHT UP MAP PROJECT
This project is based on this project, which I found on Facebook. They are commercially available here: https://metarmaps.com/. I wanted to add Canada, and a select few cities that are meaningful to me. I want to learn to solder and properly implement a reliable RPI based sym to run the final product.

<img src="Assets/Inspo.png" alt="drawing" width="200"/>

## Basis
This project is based on the Metostat library of maintained weather data across the globe.

Check out Metostat:
    https://meteostat.net/en/

Starting set of north american city coordinates courtesy of: https://www.infoplease.com/us/geography/latitude-and-longitude-us-and-canadian-cities

Futher edits and functionality beyond these two sources are built by yours truly. 

## Current State
Ability to pull weather stations from a list of starting points (city coordinates) (which has been updated to reduce iterations to find them in future reps.) and plot them on a matplotlib scatter plot. The weather station coordinates are also exported to .csv. CSV coords can easily be imported to google earth pro and viewed to validate point density (as shown below).

<img src="Assets/PLOT_OF_SELECTED.png" width=300> <img src="Assets/PLOT_OF_SELECTED_OVERLAID.png" width=200>

Functionality has been added to grab current temperatures at each of the selected weather stations, and colour map them between the High/Low temperatures in the range. RGB values are extracted to a DF to be applied to the LEDs in future works. For troubleshooting the RGB colours are plotted on a Matplotlib plot.

<img src='Assets/NA_ColourMapped_stations.png' width=400>

A base map has also been created and printed, using QGIS (https://www.qgis.org/) software, along with shapefiles of Canada, and the United States exported from fed resources (linked in the future). Basemap seen below.

<img src='Assets/BlackWhiteBasemap.png' width=400>

Added the ability to check if each station is in local daylight. Plotting on Matplotlib as semi-transparent. I did not add a debugging feature to set the time I want to check, so at the time of running, I am only pulling 3 northern stations that are not in 'daylight' locally. Will re-generate example plot below when there are more point not at daylight, either using a debugging feature or generating at a mid-sunset time.

<img src='Assets/NA_ColourMapped_stations_wDaylight.png' width =400>

## Future Works
The goal is to build this puppy. Currently narrowing down the LED dimming, changing with temperature etc. functionality as of the time of writing this README. More updates to come.


