import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]

for pin in dac:
    GPIO.setup(pin, GPIO.OUT)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def print_triangle_value(value):
    """Выводит текущее значение сигнала в виде прогресс-бара"""
    bar_length = 50
    filled = int(round(bar_length * value / 255.0))
    bar = '#' * filled + '-' * (bar_length - filled)
    sys.stdout.write(f"\rValue: {value:3d} [{bar}]")
    sys.stdout.flush()

try:
    period = float(input("Введите период треугольного сигнала в секундах: "))
    
    steps = 256
    half_period = period / 2
    step_time = half_period / steps
    
    print("Генерация треугольного сигнала (Ctrl+C для остановки)")
    
    while True:
        for value in range(255, -1, -1):
            GPIO.output(dac, dec2bin(value))
            print_triangle_value(value)
            time.sleep(step_time)
        
        for value in range(0, 256):
            GPIO.output(dac, dec2bin(value))
            print_triangle_value(value)
            time.sleep(step_time)

except KeyboardInterrupt:
    print("\nПрограмма остановлена пользователем")

except ValueError:
    print("Ошибка: введите корректное число для периода")

finally:
    GPIO.output(dac, 0)
    sys.stdout.write("\r" + " " * 80 + "\r") 
    print("Выходное значение сброшено в 0")
    GPIO.cleanup()