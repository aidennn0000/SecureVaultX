import sqlite3
import os
import hashlib

DB_PATH = "database/vault.db"
ITERATIONS = 100000


def create_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATIONS
    )

    return salt, password_hash


def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("❌ User already exists!")
        return

    salt, password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, salt, password_hash)
        VALUES (?, ?, ?)
    """, (username, salt, password_hash))

    conn.commit()
    conn.close()

    print("✅ User registered successfully!")


# =========================
# CLI INPUT (FIXED SECTION)
# =========================

print("=== SecureVaultX Registration ===")

username = input("Enter username: ").strip()
password = input("Enter password: ").strip()

# VALIDATION
if not username or not password:
    print("❌ Username and password cannot be empty!")
    exit()

register_user(username, password)
