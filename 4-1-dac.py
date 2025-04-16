import RPi.GPIO as GPIO



GPIO.setwarnings(False)

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while True:
        num = input("набери число от 0 до 255: ")
        try:
            num = int(num)
            if 0 <= num <= 255:
                str = bin(num)[2:]
                number = [0,0,0,0,0,0,0,0]
                for i in range(len(str)):
                    if(str[len(str) - i - 1] == '1'):
                        number[7-i] = 1
                GPIO.output(dac, number)
                voltage = float(num) / 256.0 * 3.3
                print(f"{voltage:.4} волт")
            else:
                if num < 0:
                    print("Число должно быть бльше 0")
                elif num > 255:
                    print("число должно быть меньше 256")  
        except Exception:
            if num == "q": break
            print("введи пожалуйста число а не строку")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()