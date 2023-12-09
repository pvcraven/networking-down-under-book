# Import the time library so we can pause the program for a specific time.
import time

# Use the Raspberry Pi library to control the general purpose input output
# (GPIO) pins.
import RPi.GPIO as GPIO

# Use a constant for our channel. Replace this
# if you want a different pin.
GPIO_CHANNEL = 17

# Use a constant for how many seconds to wait.
# You can use 0.5 if you want a half second
DELAY_TIME = 1

# State how we will specify our pin numbers.
# For a more detailed explanation, see here:
# http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/
GPIO.setmode(GPIO.BCM)

# Say we will be outputting on pin 17:
GPIO.setup(GPIO_CHANNEL, GPIO.OUT)

# Loop forever
while True:

    # Set pin 17 high. (Turn it on.)
    GPIO.output(GPIO_CHANNEL, GPIO.HIGH)
    print("LED On")

    # Wait for a second
    time.sleep(DELAY_TIME)

    # Set it low. (Turn it off.)
    GPIO.output(GPIO_CHANNEL, GPIO.LOW)
    print("LED Off")

    # Wait for a second
    time.sleep(DELAY_TIME)
