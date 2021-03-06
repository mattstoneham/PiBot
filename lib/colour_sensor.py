__author__ = 'Matt'

import RPi.GPIO as GPIO
import time


class ColourSensor(object):

    s2 = 20
    s3 = 16
    signal = 21
    NUM_CYCLES = 10
  
    def __init__(self, s2=20, s3=16, signal=21):
        self.s2 = s2
        self.s3 = s3
        self.signal = signal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.s2,GPIO.OUT)
        GPIO.setup(self.s3,GPIO.OUT)



    def get_rgb_values(self):
    
        GPIO.output(self.s2,GPIO.LOW)
        GPIO.output(self.s3,GPIO.LOW)
        #time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start      #seconds to run for loop
        red  = self.NUM_CYCLES / duration   #in Hz
        #print("red value - ",red)
    
        GPIO.output(self.s2,GPIO.LOW)
        GPIO.output(self.s3,GPIO.HIGH)
        #time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start
        blue = self.NUM_CYCLES / duration
        #print("blue value - ",blue)
    
        GPIO.output(self.s2,GPIO.HIGH)
        GPIO.output(self.s3,GPIO.HIGH)
        #time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start
        green = self.NUM_CYCLES / duration
        #print("green value - ",green)
        #print('\n\n')

        return {'red': red, 'green': green, 'blue': blue}


    def cleanup(self):
        GPIO.cleanup()


