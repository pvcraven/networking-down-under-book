# Import libraries
import time
import RPi.GPIO as GPIO

# Constants
CLOCK_LINE_PIN = 17
DATA_LINE_PIN = 12
SLEEP_TIME = 0.1

# Set up our GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(CLOCK_LINE_PIN, GPIO.OUT)
GPIO.setup(DATA_LINE_PIN, GPIO.OUT)

# Set up data
done = False
bits_in_a_byte = 8
my_message = b'Hello World'

# Loop through each byte of our message
for my_byte in my_message:

    # Show what we are encoding
    print(f"{chr(my_byte)} = {my_byte:3} = ", end="")

    # Loop for each bit of the byte, starting with the most
    # significant bit 7, down to 0.
    for bit_pos in range(bits_in_a_byte - 1, -1, -1):

        # Next line is complicated.
        # Use a single 1, and bit shift it with << to the
        # spot we are interested in. Then use a bitwise and (&)
        # and to see if that spot has a value.
        # if bit pos = 6 then
        #   1 << 6 = 0100 0000 = 64
        # if my_byte = 'H' which ASCII 72 = 0100 1000 binary
        # H      = 0100 1000
        # 1 << 6 = 0100 0000
        #          ---------
        # &      = 0100 0000 = 64 (result of bit-wise 'and')
        bit = (1 << bit_pos) & my_byte

        # Make sure bit_value is a 1 or 0, not some power of 2.
        bit_value = 0 if bit == 0 else 1

        print(bit_value, end="")

        # Turn the clock line on
        GPIO.output(CLOCK_LINE_PIN, GPIO.HIGH)

        # Turn the data line on/off depending on our data
        if bit_value == 1:
            GPIO.output(DATA_LINE_PIN, GPIO.HIGH)
        else:
            GPIO.output(DATA_LINE_PIN, GPIO.LOW)

        # Wait
        time.sleep(SLEEP_TIME)

        # Turn the clock line off, signaling it is ok to read
        # the data line now that we aren't changing it
        GPIO.output(CLOCK_LINE_PIN, GPIO.LOW)

        # Wait
        time.sleep(SLEEP_TIME)

    print()

# Reset the pins
GPIO.cleanup()
