from cryptography.fernet import Fernet

with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

password = "gmailpassword123"

encrypted = cipher.encrypt(password.encode())

print("Encrypted:")
print(encrypted)

decrypted = cipher.decrypt(encrypted)

print("\nDecrypted:")
print(decrypted.decode())
