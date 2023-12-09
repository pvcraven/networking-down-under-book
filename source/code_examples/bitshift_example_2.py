# How many bits should we encode. Usually 8, or some other multiple of 8
bits_to_encode = 8

# The b means this is a byte array.
# A byte array is different than a string. A letter in a string
# can be represented by multiple bytes. Here it can't. And this
# can have values other than letters if we really wanted.
byte_array = b'This is a message.\x00\x01\x02'
# byte_array = [i for i in range(32, 123)]

# Loop through each byte in the array
for my_byte in byte_array:

    # Now pull each bit out of the letter.
    # Start from bit 7, and count down to 0
    for bit_pos in range(bits_to_encode - 1, -1, -1):
        
        # Use bitwise and to pull out the bit we are interested in
        bit = 1 << bit_pos & my_byte
        # Convert to a 1 or 0, as the 1 may not be in the 1's place
        bit_value = 0 if bit == 0 else 1
        # Print, while staying on our current line.
        print(bit_value, end="")

    # Done with this letter. Go to the next line.
    print(f" - {my_byte:3} - {chr(my_byte)}")
