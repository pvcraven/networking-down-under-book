import time
import RPi.GPIO as GPIO

CLOCK_CHANNEL = 16
DATA_CHANNEL = 23


# This is a callback function that will be called whenever we have a high/low
# or low/high change in the signal.
def my_callback(channel):
    result = GPIO.input(DATA_CHANNEL)
    if result:
        print("1", end="")
    else:
        print("0", end="")

    my_callback.counter += 1
    if my_callback.counter > 7:
        print()
        my_callback.counter = 0


my_callback.counter = 0

# Set pin 12 up for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLOCK_CHANNEL, GPIO.IN)
GPIO.setup(DATA_CHANNEL, GPIO.IN)

# Now we have to 'register' the callback function so that the GPIO library
# will call the function when the change occurs on pin 12.
# GPIO.BOTH means it is called on both rising and falling changes.
# Use GPIO.FALLING if you want it called for high to low
# Use GPIO.RISING if you want it called low to high
GPIO.add_event_detect(CLOCK_CHANNEL, GPIO.FALLING, callback=my_callback)

# Now just wait forever.
print("Running")
while True:
    time.sleep(10)
    print("Still running")
