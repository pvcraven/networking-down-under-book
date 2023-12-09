import time
import RPi.GPIO as GPIO

GPIO_CHANNEL = 12
TIME_DELAY = 0.25

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_CHANNEL, GPIO.IN)

while True:

    # Read from pin 12. We'll get a 0 or a 1.
    result = GPIO.input(GPIO_CHANNEL)

    if result:
        # If true (1), then print high
        print("High")
    else:
        # If false (0), then print low
        print("Low")

    # Wait a quarter second before we look again
    time.sleep(TIME_DELAY)
