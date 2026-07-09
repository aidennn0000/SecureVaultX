import os
import hashlib

master_password = "MyStrongPassword123"

salt = os.urandom(16)

password_hash = hashlib.pbkdf2_hmac(
    "sha256",
    master_password.encode(),
    salt,
    100000
)

print("Salt:")
print(salt.hex())

print("\nPBKDF2 Hash:")
print(password_hash.hex())
