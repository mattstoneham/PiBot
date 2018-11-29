__author__ = 'Matt'

import threading
import time
import sys
import signal

from PiBot.lib.colour_sensor import ColourSensor
from PiBot.lib.ultrasonic_sensor import UltraSonicSensor



class MyClass(object):

    exitFlag = 0
    threads = []

    RGBsensor = {}
    distance = 0

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
            newself.RGBsensor = myColourSensor.get_rgb_values()


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

            print('\nRGB {0}'.format(self.RGBsensor))
            print('\nDistance {0}\n'.format(self.distance))
            time.sleep(1)







if __name__ == '__main__':
    cl = MyClass()

    def shutdown(sig, frame):
        for thread in cl.threads:
            thread.exit()
        sys.exit(0)


    signal.signal(signal.SIGINT, shutdown)
    cl.run()