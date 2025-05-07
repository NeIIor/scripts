# Import necessary libraries
import RPi.GPIO as GPIO  # For GPIO operations on Raspberry Pi
import matplotlib.pyplot as plt  # For plotting graphs
import time  # For time-related operations

# Function to convert number to binary (array of bits)
def dectobin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

# Function for voltage measurement using ADC
def adc():
    level = 0
    # Iterate through all bits (from MSB to LSB)
    for i in range(bits - 1, -1, -1):
        level += 2**i  # Set current bit
        GPIO.output(dac, dectobin(level))  # Output value to DAC
        time.sleep(0.01)  # Small delay
        comp_val = GPIO.input(comp)  # Read comparator value
        if comp_val == 0:  # If comparator voltage is below reference
            level -= 2**i  # Reset current bit
    return level

# Function to display value on LEDs through DAC
def num2_dac_leds(value):
    signal = dectobin(value)  # Convert number to binary
    GPIO.output(dac, signal)  # Output signal to DAC
    return signal

# Raspberry Pi pin configuration
dac = [26, 19, 13, 6, 5, 11, 9, 10]  # DAC pins
leds = [24, 25, 8, 7, 12, 16, 20, 21]  # LED pins (not used)
comp = 4  # Comparator pin
troyka = 17  # "Troyka-module" control pin
bits = len(dac)  # DAC bit count
levels = 2 ** bits  # Quantization levels
maxV = 3.3  # Maximum voltage

# GPIO initialization
GPIO.setmode(GPIO.BCM)  # Use BCM numbering

# Configure pins as input/output
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)  # "Troyka" pin as output
GPIO.setup(dac, GPIO.OUT)  # DAC pins as outputs
GPIO.setup(comp, GPIO.IN)  # Comparator pin as input

GPIO.output(troyka, 0)  # Initialize "Troyka" pin to 0

# Data storage lists
data_volts = []  # Voltage measurements
data_times = []  # Timestamps

try:
    # Experiment start
    start_time = time.time()  # Record start time
    val = 0
    print("Charging\n")
    # Capacitor charging phase
    while val < 115:
        val = adc()  # Get current ADC value
        print("volts - {:3}".format(val / levels * maxV))  # Output voltage
        num2_dac_leds(val)  # Display value on LEDs
        data_volts.append(val)  # Save voltage value
        data_times.append(time.time() - start_time)  # Save timestamp

    # Switch "Troyka" to discharge mode
    GPIO.output(troyka, 1)
    print("Discharging\n")
    # Capacitor discharging phase
    while val > 50:
        val = adc()  # Get current ADC value
        print("volts - {:3}".format(val/levels * maxV))  # Output voltage
        num2_dac_leds(val)  # Display value on LEDs
        data_volts.append(val)  # Save voltage value
        data_times.append(time.time() - start_time)  # Save timestamp

    end_time = time.time()  # Record experiment end time

    # Save settings to file
    with open("./settings.txt", "w") as file:
        file.write(str(len(data_volts) / (end_time - start_time)))  # Sampling rate
        file.write(("\n"))
        file.write(str(maxV / 256))  # ADC quantization step
    
    # Output experiment results
    print("Calculations results\n")
    print("Total time - ", end_time - start_time, " secs\n", 
          "average sampling rate - ", len(data_volts) / (end_time - start_time), "\n", 
          "single measurement period - ", (end_time - start_time)/ len(data_volts), "\n",
          "ADC quantization step - ", maxV / 256)

finally:
    # Guaranteed execution even if error occurs
    GPIO.output(dac, GPIO.LOW)  # Turn off DAC
    GPIO.output(troyka, GPIO.LOW)  # Turn off "Troyka"
    GPIO.cleanup()  # Clean up GPIO settings

# Prepare data for saving
data_times_str = [str(item) for item in data_times]
data_volts_str = [str(item) for item in data_volts]

# Save measurement data to file
with open("data.txt", "w") as file:
    file.write("\n".join(data_volts_str))

# Plot graph
plt.plot(data_times, data_volts)
plt.show()
