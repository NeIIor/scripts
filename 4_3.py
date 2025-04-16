import RPi.GPIO as GPIO
import time

# Настройка пина для ШИМ
pwm_pin = 21  # Можно изменить на другой подходящий пин
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin, GPIO.OUT)

# Создание объекта PWM с частотой 1000 Гц
pwm = GPIO.PWM(pwm_pin, 1000)  
pwm.start(0)  # Запуск с 0% заполнением

def calculate_voltage(duty_cycle):
    """Расчет выходного напряжения для RC-цепи"""
    return 3.3 * duty_cycle / 100  # 3.3V - максимальное напряжение

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