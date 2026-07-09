import sqlite3

conn = sqlite3.connect("database/vault.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    salt BLOB,
    password_hash BLOB
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    encrypted_password BLOB
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")

