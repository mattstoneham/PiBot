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
            time.sleep(updatefreq)
            newself.RGBvalues = myColourSensor.get_rgb_values()


    def findcolour(self):
        print('Raw RGB values from sensor:')
        for key, value in self.RGBvalues.items():
            print('\t'+key, value)
        print('\n')

        total = self.RGBvalues['red'] + self.RGBvalues['green'] + self.RGBvalues['blue']
        if total > self.maximum:
            print('Auto calibrated max intensity')
            maximum = total
        if total < self.minimum:
            print('Auto calibrated min intensity')
            minimum = total
        percentage = (100 / (maximum-minimum)) * (total - minimum)
        print("Light percent: {0}".format(percentage))

        if self.RGBvalues['green']<3000 and self.RGBvalues['blue']<4200 and self.RGBvalues['red']>8000:
            print("--RED--")
            temp=1
        elif self.RGBvalues['red']<2200 and  self.RGBvalues['blue']<2800 and self.RGBvalues['green']>2900:
            print("--GREEN--")
            temp=1
        elif self.RGBvalues['green']<4000 and self.RGBvalues['red']<2600 and self.RGBvalues['blue']>8400 and percentage >20:
            print("--BLUE--")
            temp=1
        elif self.RGBvalues['red']>10000 and self.RGBvalues['green']>10000 and self.RGBvalues['blue']>10000:
            print("--WHITE--")
            temp=1
        elif self.RGBvalues['red']<2000 and self.RGBvalues['green']<2000 and self.RGBvalues['blue']<2000:
            print("--BLACK--")
    
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

            #print('\nRGB {0}'.format(self.RGBsensor))
            self.findcolour()
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
    except:
        print('Exception triggered, shutting down threads')
        shutdown()