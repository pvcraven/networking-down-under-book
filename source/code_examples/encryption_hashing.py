from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64
import secrets

# Create a password and our salt
password = "mysecretpassword"
salt = secrets.token_hex(8)

# Convert to a byte array
password_bytes = password.encode("utf-8")
salt_bytes = salt.encode("utf-8")

# Create the hash
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(password_bytes)
digest.update(salt_bytes)
hashed_bytes = digest.finalize()

# Print the results
# If storing passwords in the database, store the salt and the hash.
# Don't store the password. Confirm entered passwords by hashing stored
# salt with entered password, and match against database hash.
hashed_base64 = str(base64.b64encode(hashed_bytes), encoding='utf-8')
print(f"Password: {password}")
print(f"Salt:     {salt}")
print(f"Hash:     {hashed_base64}")
