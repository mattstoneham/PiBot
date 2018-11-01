__author__ = 'Matt'


from PiBot.lib.colour_sensor import ColourSensor
import time

def main():
    maximum = 100
    minimum = 9999
    percentage = 0

    myColourSensor = ColourSensor()
    while True:
        rgbdict = myColourSensor.get_rgb_values()

        for key, value in rgbdict.items():
            print(key, value)
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

        if rgbdict['green']<3000 and rgbdict['blue']<4200 and rgbdict['red']>8000:
            print("red")
            temp=1
        elif rgbdict['red']<2200 and  rgbdict['blue']<2800 and rgbdict['green']>2900:
            print("green")
            temp=1
        elif rgbdict['green']<3700 and rgbdict['red']<2500 and rgbdict['blue']>79000 and percentage >20:
            print("blue")
            temp=1
        elif rgbdict['red']>10000 and rgbdict['green']>10000 and rgbdict['blue']>10000:
            print("white")
            temp=1
        elif rgbdict['red']<2000 and rgbdict['green']<2000 and rgbdict['blue']<2000:
            print("black")

        time.sleep(1)

if __name__=='__main__':
    main()

