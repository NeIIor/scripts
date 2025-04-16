import RPi.GPIO as GPIO
import math

dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def calculate_voltage(value):
    return 3.3 * value / 255

try:
    while True:
        user_input = input("Введите число от 0 до 255 (или 'q' для выхода): ")
        
        if user_input.lower() == 'q':
            break 
        try:
            number = int(user_input) 
            if number < 0:
                print("Ошибка: отрицательное число")
                continue  
            if number > 255:
                print("Ошибка: число превышает 255")
                continue  
            binary = decimal2binary(number)
            GPIO.output(dac, binary)
            voltage = calculate_voltage(number)
            print(f"Предполагаемое напряжение: {voltage:.2f} В")
        except ValueError:
            print("Ошибка: введено не числовое значение")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()