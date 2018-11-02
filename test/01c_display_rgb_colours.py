__author__ = 'Matt'


from PiBot.lib.colour_sensor import ColourSensor
from PiBot.lib.rgb_led import *
import time

def main():

    def remap(value):
        return (100 / 17000) * value

    maximum = 100
    minimum = 9999
    percentage = 0

    myColourSensor = ColourSensor()
    rgbled = RGBLed(18, 23, 24)

    while True:
        rgbdict = myColourSensor.get_rgb_values()
        print('Raw RGB values from sensor:')
        for key, value in rgbdict.items():
            print('\t'+key, value)
        print('\n')

        total = rgbdict['red'] + rgbdict['green'] + rgbdict['blue']
        if total > maximum:
            print('Auto calibrated max intensity')
            maximum = total
        if total < minimum:
            print('Auto calibrated min intensity')
            minimum = total
        percentage = (100 / (maximum-minimum)) * (total - minimum)
        print("Light percent: {0}".format(percentage))

        rgbled.set_color((remap(rgbdict['red']), remap(rgbdict['green']), remap(rgbdict['green'])))

        time.sleep(.5)

if __name__=='__main__':
    main()

