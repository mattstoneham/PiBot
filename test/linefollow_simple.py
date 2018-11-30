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
            total = newself.RGBvalues['red'] + newself.RGBvalues['green'] + newself.RGBvalues['blue']
            if total > newself.maximum:
                print('Auto calibrated max intensity')
                newself.maximum = total
            if total < newself.minimum:
                print('Auto calibrated min intensity')
                newself.minimum = total
            try:
                newself.percentage = (100 / (newself.maximum - newself.minimum)) * (total - newself.minimum)
            except:
                pass # handle potential divide by zero on start
            #print("Light percent: {0}".format(percentage))

            if newself.RGBvalues['green']<3000 and newself.RGBvalues['blue']<4200 and newself.RGBvalues['red']>8000:
                newself.colour = 'RED'
                #print("--RED--")
            elif newself.RGBvalues['red']<2200 and  newself.RGBvalues['blue']<2800 and newself.RGBvalues['green']>2900:#
                newself.colour = 'GREEN'
                #print("--GREEN--")
            elif newself.RGBvalues['green']<4000 and newself.RGBvalues['red']<2600 and newself.RGBvalues['blue']>8400:
                newself.colour = 'BLUE'
                #print("--BLUE--")
            elif newself.RGBvalues['red']>8000 and newself.RGBvalues['green']>8000 and newself.RGBvalues['blue']>8000:
                newself.colour = 'WHITE'
                #print("--WHITE--")
            elif newself.RGBvalues['red']<2000 and newself.RGBvalues['green']<2000 and newself.RGBvalues['blue']<2000:
                newself.colour = 'BLACK'
                #print("--BLACK--")



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

            #self.findcolour()
            print('\n\nRGB Colour: {0}  Light percent: {1}'.format(self.colour, self.percentage))
            print('Distance {0}\n'.format(self.distance))
            if self.colour == None:
                print('Looking for the line (unspecified colour)')

            if self.colour == 'BLACK':
                print('Following line')
                rrb3.set_motors(0.3, 0, 0.2, 0)
                #print('Arc right')
                #rrb3.set_motors(0.4, 0, 0.2, 0)

            if self.colour == 'BLACK':
                print('Searching for line')
                rrb3.right(speed=0.2)
                #print('Arc left')
                #rrb3.set_motors(0.2, 0, 0.4, 0)







if __name__ == '__main__':
    cl = MyClass()
    rrb3 = RRB3()

    def shutdown(sig=None, frame=None):
        for thread in cl.threads:
            thread.exit()
        rrb3.stop()
        sys.exit(0)


    signal.signal(signal.SIGINT, shutdown)
    try:
        cl.run()
    except Exception as e:
        print(e)
        print('Exception triggered, shutting down threads')
        shutdown()
