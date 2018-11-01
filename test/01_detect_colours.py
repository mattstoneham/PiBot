__author__ = 'Matt'

from lib.colour_sensor import ColourSensor as cs
import time

def main():
    while True:
        rbgdict = cs.get_rgb_values()

        for key, value in rbgdict.items():
            print(key, value)

        time.sleep(1)

if __name__ == 'main':
    main()


