""" AES Encryption Example """

# This example uses the "cryptography" example.
# pip/pip3 install cryptography
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Create a 32 byte (256 bit) key
key = os.urandom(32)
print("Key:", key.hex())

# Create a 16 byte (128 bit) initialization vector
# Look up AES Initialization Vector for more info
init_vector = os.urandom(16)
print("IV: ", init_vector.hex())

# Set up our cipher
# CBC stands for Ciphertext Block Chaining where each plaintext block
# is XOR'd with the prior block. The IV is XOR'd with the first block.
# The other option is Electronic Codebook (EBC)
# where each block is independent of each other block. This is not as secure.
backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.CBC(init_vector), backend=backend)
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Create our secret message
secret_message = "This is my secret message."

# Convert to bytes
secret_message_bytes = secret_message.encode("UTF-8")

# Pad the array with spaces to our block length.
while len(secret_message_bytes) % 16 != 0:
    secret_message_bytes += b' '

# Encrypt
# The result is a byte array that isn't directly printable without
# converting to hex-text or base64.
ct = encryptor.update(secret_message_bytes) + encryptor.finalize()
print("Encrypted message in hex:   ", ct.hex())
print("Encrypted message in Base64:", base64.b64encode(ct).decode("utf-8"))

# Decrypt
result = decryptor.update(ct) + decryptor.finalize()

# Convert from bytes to a string
plain_text = result.decode("UTF-8")

# Print result
print(f"Decrypted message: '{plain_text}'")
