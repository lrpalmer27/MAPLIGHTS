### THIS FILE IS INTENDED TO BE RUN ON RPI
"""
THE OBJECTIVE OF THIS SCRIPT IS TO BE THE MAIN RUNNING SCRIPT ON THE PI
    - IT WILL START BY QUERYING THE PKL FILE GENERATED ON PC.
    - EVENTUALLY THE 'MAIN' FILE WILL BE CONVERTED TO A CALLABLE METHOD AND RUN ENTIRELY ON PI. POTENTIALLY SAVE PKL FOR ACCESS WHILE RERUNNING. 
    
FUNCTIONALITY
    - SHOULD IMPORT COLORS RELATING TO TEMPERATURES.
    - SHOULD IMPORT LOCAL SUNSET STATUS

"""

import time
import os
from datetime import datetime, timedelta, date, timezone
from rpi_ws281x import *
import argparse
import pandas as pd
from DATAGENERATOR import GENERATEDATA
from suntime import Sun, SunTimeException

# LED strip configuration:
LED_COUNT      = 138     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 10      # Set to 0 for darkest and 255 for brightest - THIS IS MAPPED LATER. USE THIS AS A GLOBAL BRIGHTNESS MODIFIER.
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def QuickLoop(Data,strip,startingTime,cUTCtime,BuildLocationSunrise,BuildLocationSunset,LOOPDURATION):
    while cUTCtime + timedelta(hours=LOOPDURATION) > startingTime: #this opens a while loop for 1 hour.
        # # Check current time.
        cUTCtime=datetime.now(timezone.utc)
        
        if BuildLocationSunrise<=cUTCtime>=BuildLocationSunset:
            localDaylight=1
        else:
            localDaylight=0.75 #Use this to modify how much less bright it gets.
            
        # # Go though each row in pkl df and determine colour considerate of local and station sunset times. 
        for rowN in range(0,len(Data.Sunrise)):
            if Data.Sunrise[rowN]<=cUTCtime<=Data.Sunset[rowN]:
                #daylight in that locaton
                stationdayli=1
            else:
                #not daylight in that locaton. Use this to modify how much less bright it gets.
                stationdayli=0.75
           
            #get the 0-1 range rgb value in pkl df and convert to a brightness considerate.    
            ConsiderateRGBA=(pd.Series(Data.RGBA[rowN])*255*stationdayli*localDaylight).tolist()

            strip.setPixelColor(rowN,Color(int(ConsiderateRGBA[0]),int(ConsiderateRGBA[1]),int(ConsiderateRGBA[2])))
            # strip.setPixelColor(Data.OrderedIndex[rowN],Color(ConsiderateRGBA[0],ConsiderateRGBA[1],ConsiderateRGBA[2])) #use when ordered index is actually correct.
            strip.show()
        
        print('quickloop reloop')
        time.sleep(60) #rest 60s before looping again
    
def theaterChase(strip, color, wait_ms=50, iterations=5):
    """Movie theater light style chaser animation."""
    """This is more like a sparkle action"""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
def InitializationAnimations(strip):
    theaterChase(strip, Color(127, 127, 127)) #white sparkle
    colorWipe(strip, Color(127,127,127)) #white light chase
    colorWipe(strip, Color(0,0,0),wait_ms=1) #LIGHTS OUT!
    colorWipe(strip, Color(0,0,127)) #blue lights
    colorWipe(strip, Color(0,0,0),wait_ms=1) #LIGHTS OUT!
    colorWipe(strip, Color(0,127,0)) #green lights
    colorWipe(strip, Color(0,0,0),wait_ms=1) #LIGHTS OUT!
    colorWipe(strip, Color(127,0,0)) #red lights
    colorWipe(strip, Color(0,0,0),wait_ms=1) #LIGHTS OUT!

# Main program logic follows:
if __name__ == '__main__':
    # ------------------------------------------------- INIT ITEMS -----------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    ## ------------------------------------------------- INITIAL ANIMATIONS HERE -----------------------------------------------------------
    
    print('Initalization - Color Wipes')
    InitializationAnimations(strip)
         
    ## ------------------------------------------------- MAIN LOOP HERE -----------------------------------------------------------
    while True: # Never stop!!!
        print('Query weather stations for new data!')
        GENERATEDATA()
        print('New data saved')
               
        # # Import the current data pickle file.
        Data=pd.read_pickle(os.path.join(os.getcwd(),'cDATA.pkl'))
        
        # initialize time variables
        startingTime=datetime.now(timezone.utc)
        cUTCtime=datetime.now(timezone.utc)

        # # Get sunrise/sunset time in Dallas (approx build location)
        sun=Sun(32.7767,-96.7970) #dallas coords
        BuildLocationSunrise=sun.get_local_sunrise_time(time_zone=timezone.utc)
        BuildLocationSunset=sun.get_local_sunset_time(time_zone=timezone.utc)
        
        # Play some animations right before displaying the new colors.
        theaterChase(strip, Color(127, 127, 127))
        colorWipe(strip, Color(0,0,0),wait_ms=1) #lights out
        
        print('Open loop to show colors and brightnesses but not recheck temps')
        # open quickloop function, looping quicker, intention is to catch sunrise/sunset times.
        QuickLoop(Data,strip,startingTime,cUTCtime,BuildLocationSunrise,BuildLocationSunset,LOOPDURATION=1)
        
        
        