import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from theme import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "vault.db")
ITERATIONS = 100000


# ================= DATABASE =================

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


# ================= DASHBOARD =================

def open_dashboard(username):
    root.destroy()
    subprocess.Popen(
        ["python3", "gui/dashboard_gui_v2.py", username]
    )
# ================= PASSWORD TOGGLE =================

show_password = False

def toggle_password():
    global show_password

    if show_password:
        password_entry.config(show="*")
        show_button.config(text="Show")
        show_password = False
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")
        show_password = True


# ================= LOGIN =================

def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror(
            "Error",
            "Username and password cannot be empty!"
        )
        return

    user = get_user(username)

    if not user:
        messagebox.showerror(
            "Error",
            "User not found!"
        )
        return

    stored_username, salt, stored_hash = user

    if verify_password(salt, stored_hash, password):
        messagebox.showinfo(
            "Success",
            "Login successful!"
        )
        open_dashboard(username)
    else:
        messagebox.showerror(
            "Error",
            "Incorrect password!"
        )


# ================= WINDOW =================

root = tk.Tk()
root.title("LOGIN V2 TEST")
root.geometry("900x600")
root.resizable(False, False)
root.configure(bg=BACKGROUND)


# ================= LOGIN CARD =================

card = tk.Frame(
    root,
    bg=CARD,
    width=420,
    height=450,
    highlightbackground=BORDER,
    highlightthickness=1
)

card.place(relx=0.5, rely=0.5, anchor="center")
card.pack_propagate(False)


# ================= TITLE =================

title = tk.Label(
    card,
    text="🔐 LOGIN GUI V2",
    bg=CARD,
    fg=TEXT,
    font=TITLE_FONT
)

title.pack(pady=(25, 5))

subtitle = tk.Label(
    card,
    text="Encrypted Password Manager",
    bg=CARD,
    fg=SECONDARY_TEXT,
    font=TEXT_FONT
)

subtitle.pack(pady=(0, 25))


# ================= USERNAME =================

username_label = tk.Label(
    card,
    text="Username",
    bg=CARD,
    fg=TEXT,
    font=TEXT_FONT
)

username_label.pack(anchor="w", padx=40)

username_entry = tk.Entry(
    card,
    width=32,
    font=("Segoe UI", 11)
)

username_entry.pack(pady=8)


# ================= PASSWORD =================

password_label = tk.Label(
    card,
    text="Password",
    bg=CARD,
    fg=TEXT,
    font=TEXT_FONT
)

password_label.pack(anchor="w", padx=40)

password_entry = tk.Entry(
    card,
    width=32,
    font=("Segoe UI", 11),
    show="*"
)

password_entry.pack(pady=8)


# ================= SHOW BUTTON =================

show_button = tk.Button(
    card,
    text="Show",
    command=toggle_password,
    bg="#DDDDDD",
    width=10
)

show_button.pack(pady=5)


# ================= LOGIN BUTTON =================

login_button = tk.Button(
    card,
    text="Login Securely",
    command=login,
    bg=PRIMARY,
    fg="white",
    font=BUTTON_FONT,
    width=22,
    height=2,
    bd=0,
    cursor="hand2"
)

login_button.pack(pady=20)


# ================= FOOTER =================

footer = tk.Label(
    card,
    text="AES Encryption • PBKDF2 Authentication",
    bg=CARD,
    fg=SECONDARY_TEXT,
    font=FOOTER_FONT
)

footer.pack(side="bottom", pady=20)


root.mainloop()
