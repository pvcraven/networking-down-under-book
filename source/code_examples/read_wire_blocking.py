import RPi.GPIO as GPIO

GPIO_CHANNEL = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_CHANNEL, GPIO.IN)

print("Waiting...")
while True:

    # Wait for pin 12 to go high
    result = GPIO.wait_for_edge(GPIO_CHANNEL, GPIO.RISING)
    print("High")

    # Now wait for it to go low
    result = GPIO.wait_for_edge(GPIO_CHANNEL, GPIO.FALLING)
    print("Low")
