__author__ = 'Matt'

import threading
import time
import sys
import signal

from PiBot.lib.colour_sensor import ColourSensor
from PiBot.lib.ultrasonic_sensor import UltraSonicSensor
from PiBot.lib.rrb3 import *



class MyClass(object):

    exitFlag = 0
    threads = []

    RGBvalues = {}
    distance = 0
    
    maximum = 100
    minimum = 9999
    percentage = 0
    colour = 'None'

    class SensorThread(threading.Thread):
        def __init__(self, name, threadID, sensortype, updatefreq=0.5):
            threading.Thread.__init__(self)
            self.name = name
            self.updatefreq = updatefreq
            self.sensortype = sensortype

        def run(self):
            print("Starting " + self.name)
            if self.sensortype == 'RGB':
                MyClass().getRGBsensorvalue(MyClass, self.updatefreq)
            if self.sensortype == 'Ultrasonic':
                MyClass().getUltrasonicSensorvalue(MyClass, self.updatefreq)
            print("Exiting " + self.name)

        def exit(self):
            MyClass.exitFlag = 1

    def getUltrasonicSensorvalue(self, newself, updatefreq):
        myUltrasonicSensor = UltraSonicSensor()
        while not newself.exitFlag:
            time.sleep(updatefreq)
            newself.distance = myUltrasonicSensor.get_distance()

    def getRGBsensorvalue(self, newself, updatefreq):
        myColourSensor = ColourSensor()
        while not newself.exitFlag:
            time.sleep(0.1)
            newself.RGBvalues = myColourSensor.get_rgb_values()


    def findcolour(self):
        try:
            #print('Raw RGB values from sensor:')
            #for key, value in self.RGBvalues.items():
            #    print('\t'+key, value)
            #print('\n')

            total = self.RGBvalues['red'] + self.RGBvalues['green'] + self.RGBvalues['blue']
            if total > self.maximum:
                print('Auto calibrated max intensity')
                self.maximum = total
            if total < self.minimum:
                print('Auto calibrated min intensity')
                self.minimum = total
            self.percentage = (100 / (self.maximum - self.minimum)) * (total - self.minimum)
            #print("Light percent: {0}".format(percentage))

            if self.RGBvalues['green']<3000 and self.RGBvalues['blue']<4200 and self.RGBvalues['red']>8000:
                self.colour = 'RED'
                #print("--RED--")
            elif self.RGBvalues['red']<2200 and  self.RGBvalues['blue']<2800 and self.RGBvalues['green']>2900:#
                self.colour = 'GREEN'
                #print("--GREEN--")
            elif self.RGBvalues['green']<4000 and self.RGBvalues['red']<2600 and self.RGBvalues['blue']>8400 and self.percentage >20:
                self.colour = 'BLUE'
                #print("--BLUE--")
            elif self.RGBvalues['red']>10000 and self.RGBvalues['green']>10000 and self.RGBvalues['blue']>10000:
                self.colour = 'WHITE'
                #print("--WHITE--")
            elif self.RGBvalues['red']<2000 and self.RGBvalues['green']<2000 and self.RGBvalues['blue']<2000:
                self.colour = 'BLACK'
                #print("--BLACK--")
        except:
            print('No RGB sensor values yet!')
    
    def run(self):
        # Create new threads
        # Create the RGB sensor thread
        self.threads.append(self.SensorThread('RGBSensorThread', 1, 'RGB', 0.5))
        # Create the ultrasonic sensor thread
        self.threads.append(self.SensorThread('UltrasonicSensorThread', 2, 'Ultrasonic', 0.5))

        # Start the threads
        for thread in self.threads:
            print('Starting thread: {0}'.format(thread))
            thread.start()
            print('\tdone!')


        while not self.exitFlag:

            # Control our bot based on sensor values here!

            self.findcolour()
            print('\nRGB Colour: {0}\tLight percent: {1}'.format(self.colour, self.percentage))
            print('\nDistance {0}\n'.format(self.distance))
            time.sleep(1)







if __name__ == '__main__':
    cl = MyClass()

    def shutdown(sig=None, frame=None):
        for thread in cl.threads:
            thread.exit()
        sys.exit(0)


    signal.signal(signal.SIGINT, shutdown)
    try:
        cl.run()
    except Exception as e:
        print(e)
        print('Exception triggered, shutting down threads')
        shutdown()