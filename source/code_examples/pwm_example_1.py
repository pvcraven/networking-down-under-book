import RPi.GPIO as GPIO
import time

# Specify pin numbers by boadcom SOC channel
GPIO.setmode(GPIO.BCM)

# Constants
gpio_channel = 17
pwm_frequency = 1
duty_start = 0
duty_end = 100
time_gap = 2
increment = 5

# Set channel for output
GPIO.setup(gpio_channel, GPIO.OUT)

# Tell Pi to use channel for PWM
p = GPIO.PWM(gpio_channel, pwm_frequency)

# Start the PWM with our initial value
p.start(duty_start)

# Cycle back and forth
for i in range(10):

    # Move counter-clockwise
    for duty_cycle in range(duty_start, duty_end, increment):
        p.ChangeDutyCycle(duty_cycle)
        print("Duty cycle:", duty_cycle)
        time.sleep(time_gap)

        # Move clock-wise
    for duty_cycle in range(duty_end, duty_start, -increment):
        p.ChangeDutyCycle(duty_cycle)
        print("Duty cycle:", duty_cycle)
        time.sleep(time_gap)

p.stop()
