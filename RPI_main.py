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
from rpi_ws281x import *
import Adafruit_NeoPixel 
import argparse

# LED strip configuration:
LED_COUNT      = 2     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest - THIS IS MAPPED LATER.
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

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

    ## ------------------------------------------------- MAIN LOOP HERE -----------------------------------------------------------
    
    # TODO:
    """
    1. get current time in gmt
    2. import pkl file with temperatures
    3. compare current time to sunset time in each location, map brightness lower if the sun has set locally
    4. Map ALL brightnesses lower by a % when current time zone sunset has passed.
    
    """
    
    
    strip.setPixelColor(1,Color(255,0,0))
    strip.show()