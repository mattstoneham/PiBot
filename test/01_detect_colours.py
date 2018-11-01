__author__ = 'Matt'


from PiBot.lib.colour_sensor import ColourSensor
import time

def main():
    myColourSensor = ColourSensor()
    while True:
        rbgdict = myColourSensor.get_rgb_values()

        for key, value in rbgdict.items():
            print(key, value)

        time.sleep(1)

if __name__=='__main__':
    main()

