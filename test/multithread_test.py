__author__ = 'Matt'

import threading
import time
import sys
import signal

import RPi.GPIO as GPIO
from PiBot.lib.colour_sensor import ColourSensor

class MyClass(object):

    exitFlag = 0
    value = 0
    threadID = ''
    name = ''
    thread1 = ''

    RGBsensor = {}

    class SensorThread(threading.Thread):
        def __init__(self, threadID, name, updatefreq=0.5):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.updatefreq = updatefreq

        def run(self):
            print("Starting " + self.name)
            MyClass().getsensorvalue(MyClass, self.updatefreq)
            print("Exiting " + self.name)

        def exit(self):
            MyClass.exitFlag = 1



    def getsensorvalue(self, newself, updatefreq):
        myColourSensor = ColourSensor()
        while not newself.exitFlag:
            time.sleep(updatefreq)
            newself.RGBsensor = myColourSensor.get_rgb_values()


    def run(self):
        # Create new threads
        self.thread1 = self.SensorThread('MySensorThread', 1, 0.5)
        print('thread1 = {0}'.format(self.thread1))
        self.thread1.start()


        while not self.exitFlag:
            print('\nRGB {0}'.format(self.RGBsensor))







if __name__ == '__main__':
    cl = MyClass()

    def signal_handler(sig, frame):
        cl.thread1.exit()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    cl.run()