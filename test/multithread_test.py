__author__ = 'Matt'

import threading
import time
import sys
import signal

from PiBot.lib.colour_sensor import ColourSensor
from PiBot.lib.ultrasonic_sensor import UltraSonicSensor



class MyClass(object):

    exitFlag = 0
    #value = 0
    #threadID = ''
    #name = ''
    threads = []

    RGBsensor = {}
    distance = 0

    class SensorThread(threading.Thread):
        def __init__(self, name, threadID, sensortype, updatefreq=0.5):
            threading.Thread.__init__(self)
            #self.threadID = threadID
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
        self.threads.append(self.SensorThread('RGBSensorThread', 1, 'RGB', 0.5))
        self.threads.append(self.SensorThread('UltrasonicSensorThread', 2, 'Ultrasonic', 0.5))

        #print('thread1 = {0}'.format(self.thread1))
        for thread in self.threads:
            print('Starting thread: {0}'.format(thread))
            thread.start()
            print('\tdone!')


        while not self.exitFlag:
            print('\nRGB {0}'.format(self.RGBsensor))







if __name__ == '__main__':
    cl = MyClass()

    def signal_handler(sig, frame):
        #cl.thread1.exit()
        for thread in cl.threads:
            print('Stopping thread: {0}'.format(thread))
            thread.exit()
            print('\tdone!')
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    cl.run()