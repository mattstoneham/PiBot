__author__ = 'Matt'

import threading
import time
import sys
import signal

class MyClass(object):

    exitFlag = 0
    value = 0
    threadID = ''
    name = ''
    thread1 = ''

    class SensorThread(threading.Thread):
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name

        def run(self):
            print("Starting " + self.name)
            MyClass().getsensorvalue(MyClass)
            print("Exiting " + self.name)

        def exit(self):
            MyClass.exitFlag = 1


    def getsensorvalue(self, newself):
        while not newself.exitFlag:
            newself.value += 1
            if newself.value > 4999:
                newself.exitFlag = 1
            print('self.value: {0}'.format(newself.value))


    def run(self):
        # Create new threads
        self.thread1 = self.SensorThread('MySensorThread', 1)
        print('thread1 = {0}'.format(self.thread1))
        self.thread1.start()


        while not self.exitFlag:
            print('Hello there self.value of {0}'.format(self.value))







if __name__ == '__main__':
    cl = MyClass()

    def signal_handler(sig, frame):
        cl.thread1.exit()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    cl.run()