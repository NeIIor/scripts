import RPi.GPIO as GPIO
import time

def bin_translator(num, delay):
    number = [0, 0, 0, 0, 0, 0, 0, 0]
    kr = num % 256
    binch = bin(kr)
    i = -1
    while binch[i] != 'b':
        number[i] = int(binch[i])
        i -= 1

    print("[] --> {}".format(num, number))

    GPIO.output(dac, number)
    volt = float(input())
    voltage.append(volt)
    return 0

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
voltage = []

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

nums = [0, 5, 32, 64, 127, 255, 256]

for i in nums:
    bin_translator(i, 10)

print(voltage)

GPIO.output(dac, 0)
GPIO.cleanup()