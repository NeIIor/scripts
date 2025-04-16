import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]  
GPIO.setup(dac, GPIO.OUT)

def dec2bin(num):
    str = bin(num)[2:]
    number = [0,0,0,0,0,0,0,0]
    for i in range(len(str)):
        if(str[len(str) - i - 1] == '1'):
            number[7-i] = 1
    return number

try:
    num = 0
    direction = 1

    while True:
        GPIO.output(dac, dec2bin(num))
        time.sleep(3.0/512) 
        print(num)
        num += direction
        if num >= 255:
            direction = -1
        elif num <= 0:
            direction = 1

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()