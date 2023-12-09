from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

# Create public/private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Print the private key in PEM format
private_key_decoded = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
print(private_key_decoded)

# Print the public key in PEM format
public_key_decoded = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()
print(public_key_decoded)

# Create our message as a string, and encode in a byte array
message = "I propose to consider the question, 'Can machines think?'"
message_bytes = bytes(message, encoding='utf-8')

# Encrypt the data, and auto-pad it to multiples of 256 bytes
encrypted_data = public_key.encrypt(
    message_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Print the encrypted data in base64 format which can be
# copy/pasted.
cipher_text_base64 = str(base64.b64encode(encrypted_data), encoding='utf-8')
print(cipher_text_base64)

# Unencrypt the data
unencrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Convert the byte array to a string array
plain_text = unencrypted_data.decode("UTF-8")
print(plain_text)
