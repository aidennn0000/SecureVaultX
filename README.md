# SecureVaultX

SecureVaultX is an open-source password manager developed in Python using Tkinter and SQLite.

## Features

- User Registration and Login
- PBKDF2 Password Hashing
- AES/Fernet Encryption
- Password Generator
- Secure Password Storage
- Auto Logout after 5 minutes of inactivity
- GUI-based Password Vault

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/SecureVaultX.git
cd SecureVaultX
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 main.py
```

## Technologies Used

- Python
- Tkinter
- SQLite
- Cryptography Library

## Security Features

- PBKDF2-HMAC-SHA256 password hashing
- Salted password storage
- AES encryption via Fernet
- Automatic session timeout
- Strong password generation

## Author

Bibash Bhatta
