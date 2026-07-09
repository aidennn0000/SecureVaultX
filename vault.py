import sqlite3
from cryptography.fernet import Fernet

DB_PATH = "database/vault.db"

# Load encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)


def add_password(website, username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    encrypted_password = cipher.encrypt(password.encode())

    cursor.execute("""
        INSERT INTO vault (website, username, encrypted_password)
        VALUES (?, ?, ?)
    """, (website, username, encrypted_password))

    conn.commit()
    conn.close()

    print("✅ Password saved securely!")


def view_passwords():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT website, username, encrypted_password FROM vault")
    rows = cursor.fetchall()

    print("\n=== STORED PASSWORDS ===")

    for website, username, encrypted_password in rows:
        decrypted_password = cipher.decrypt(encrypted_password).decode()

        print("\nWebsite:", website)
        print("Username:", username)
        print("Password:", decrypted_password)

    conn.close()


# ======================
# CLI MENU
# ======================

print("=== SecureVaultX Vault System ===")

print("\n1. Add Password")
print("2. View Passwords")

choice = input("\nEnter choice: ")

if choice == "1":
    website = input("Website: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not website or not username or not password:
        print("❌ All fields are required!")
        exit()

    add_password(website, username, password)

elif choice == "2":
    view_passwords()

else:
    print("❌ Invalid choice")
