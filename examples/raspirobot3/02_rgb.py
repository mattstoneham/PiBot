# 02_rgb.py
# Turn on the RGB LED colours for 1 second each
import RPi.GPIO as GPIO
from PiBot.lib.rgb_led import *
import time

rgbled = RGBLed(18, 23, 24)

try:
    while True:
        rgbled.set_color(RED)
        time.sleep(1)
        rgbled.set_color(GREEN)
        time.sleep(1)
        rgbled.set_color(BLUE)
        time.sleep(1)
        
finally: 
    GPIO.cleanup()
