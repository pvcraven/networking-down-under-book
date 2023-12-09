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

    # If the interval is greater than three clock cycles, this must be a new message
    if time_interval > CLOCK_SPEED * 3:
        data_callback.data_bit = True
        print("---")

    elif time_interval > CLOCK_SPEED + CLOCK_SPEED / 2 or data_callback.data_bit:
        data_callback.data_bit = False
        if data_line == 0:
            print(" Bit {} is 0".format(data_callback.bit_count))
        else:
            print(" Bit {} is 1".format(data_callback.bit_count))
            data_callback.my_byte += 1 << data_callback.bit_count

        data_callback.bit_count -= 1
        if data_callback.bit_count == -1:
            my_char = chr(data_callback.my_byte)
            print("Got: {:3} -> {}".format(data_callback.my_byte, my_char))
            data_callback.bit_count = 7
            data_callback.my_byte = 0
    else:
        data_callback.data_bit = True

    data_callback.last_call = cur_time

data_callback.data_bit = False
data_callback.last_call = time.time()
data_callback.bit_count = 7
data_callback.my_byte = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_DATA_IN, GPIO.IN)
GPIO.add_event_detect(GPIO_DATA_IN, GPIO.BOTH, callback=data_callback)

print("Running")
while True:
    time.sleep(10)

