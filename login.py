import sqlite3
import hashlib

DB_PATH = "database/vault.db"
ITERATIONS = 100000


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, salt, password_hash FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def verify_password(stored_salt, stored_hash, password_attempt):
    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_attempt.encode(),
        stored_salt,
        ITERATIONS
    )

    return new_hash == stored_hash


# =========================
# CLI LOGIN (FIXED VERSION)
# =========================

print("=== SecureVaultX Login ===")

username = input("Enter username: ").strip()
password = input("Enter password: ").strip()

# SECURITY FIX (IMPORTANT)
if not username or not password:
    print("❌ Username and password cannot be empty!")
    exit()

# Fetch user
user = get_user(username)

if not user:
    print("❌ User not found!")
    exit()

stored_username, salt, stored_hash = user

# Verify password
if verify_password(salt, stored_hash, password):
    print("✅ Login successful!")
else:
    print("❌ Incorrect password!")
