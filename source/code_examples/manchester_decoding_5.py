"""
Manchester Decoding

Receives a message sent by Manchester Encoding
"""
import time
import RPi.GPIO as GPIO

GPIO_DATA_IN = 13
CLOCK_SPEED = .005


def data_callback(channel):
    """
    Called when we get a transition from low to high or high to low.
    Registered by the GPIO.add_event_detect() call after this function.
    """
    # Get data line value
    data_line = GPIO.input(GPIO_DATA_IN)

    # Get time interval
    cur_time = time.time()
    time_interval = cur_time - data_callback.last_call

    # If the interval is greater than three clock cycles, this must be a new message
    if time_interval > CLOCK_SPEED * 3:
        data_callback.data_bit = True
        print("---")

    # Is this transition a data bit?
    # If data_bit is True, it is.
    # If we waited at least 1.5 clock cycles, it has to be a data bit
    elif time_interval > CLOCK_SPEED + CLOCK_SPEED / 2 or data_callback.data_bit:
        # Next transition may or may not be a data bit.
        data_callback.data_bit = False

        # Is the line high (low to high)? If so, we have a 1.
        if data_line != 0:
            # Take a one, shift into proper place, add to our result
            data_callback.my_byte += 1 << data_callback.bit_count

        # Move our bit position down one. (7 down to 0)
        data_callback.bit_count -= 1
        # Have we received every bit?
        if data_callback.bit_count == -1:
            # Convert to character and print
            my_char = chr(data_callback.my_byte)
            print("Got: {:3} -> {}".format(data_callback.my_byte, my_char))
            # Reset
            data_callback.bit_count = 7
            data_callback.my_byte = 0
    else:
        # Ok, if this wasn't a data transition, the next one has to be.
        data_callback.data_bit = True

    # Grab timestamp of this transition
    data_callback.last_call = cur_time


# --- Function variable
# If true, next transition has to represent a bit. If false, it may or may not.
data_callback.data_bit = False
# Time stamp of the last transition
data_callback.last_call = time.time()
# Current bit we are on
data_callback.bit_count = 7
# Current byte, with all 8 bits
data_callback.my_byte = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_DATA_IN, GPIO.IN)

# Register the data_callback function to be called if we detect a transition
# in the data line.
GPIO.add_event_detect(GPIO_DATA_IN, GPIO.BOTH, callback=data_callback)

print("Running")
while True:
    time.sleep(10)

