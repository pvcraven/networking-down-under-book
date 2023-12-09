"""
Manchester Decoding

Receives a message sent by Manchester Encoding
"""
import time
import RPi.GPIO as GPIO

GPIO_DATA_IN = 13
CLOCK_SPEED = .005

def data_callback(channel):

    # Get data line value
    data_line = GPIO.input(GPIO_DATA_IN)

    # Get time interval
    cur_time = time.time()
    time_interval = cur_time - data_callback.last_call

    dl = "L->H" if data_line else "H->L"
    print("  Change: {} Interval: {:.3f}".format(dl, time_interval))

    if time_interval > CLOCK_SPEED + CLOCK_SPEED / 2 or data_callback.data_bit:
        data_callback.data_bit = False
        if data_line == 0:
            print("0")
        else:
            print("1")
    else:
        data_callback.data_bit = True

    data_callback.last_call = cur_time

data_callback.data_bit = False
data_callback.last_call = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_DATA_IN, GPIO.IN)
GPIO.add_event_detect(GPIO_DATA_IN, GPIO.BOTH, callback=data_callback)

print("Running")
while True:
    time.sleep(10)

