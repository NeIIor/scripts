import RPi.GPIO as GPIO
import time

pwm_pin = 22 
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)

pwm = GPIO.PWM(pwm_pin, 1000)  
pwm.start(0)  

def calculate_voltage(duty_cycle):
    return 3.3 * duty_cycle / 100 

try:
    print("ШИМ-генератор с расчетом напряжения")
    print("Управление RC-цепью (0-100%)")
    print("Для выхода нажмите Ctrl+C\n")
    
    while True:
        try:
            duty = float(input("Введите коэффициент заполнения (0-100%): "))
            
            if duty < 0 or duty > 100:
                print("Ошибка: значение должно быть от 0 до 100!")
                continue
                
            pwm.ChangeDutyCycle(duty)
            voltage = calculate_voltage(duty)
            print(f"Расчетное напряжение: {voltage:.2f} В\n")
            
        except ValueError:
            print("Ошибка: введите число от 0 до 100!")

except KeyboardInterrupt:
    print("\nПрерывание пользователем")
finally:
    pwm.stop()
    GPIO.cleanup()
    print("ШИМ остановлен, GPIO очищен")