import tkinter as tk
from tkinter import messagebox
import os
import sys
import secrets
import string

sys.path.append(os.path.abspath(".."))
from theme import *

root = tk.Tk()

root.title("SecureVaultX Password Generator")
root.geometry("700x750")
root.configure(bg=BACKGROUND)
root.resizable(False, False)

# =============================
# Header
# =============================

header = tk.Frame(root, bg=PRIMARY, height=60)
header.pack(fill="x")

tk.Label(
    header,
    text="🔑 Password Generator",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 18, "bold")
).pack(pady=15)

# =============================
# Generate Password
# =============================

def generate_password():

    characters = ""

    if upper_var.get():
        characters += string.ascii_uppercase

    if lower_var.get():
        characters += string.ascii_lowercase

    if number_var.get():
        characters += string.digits

    if symbol_var.get():
        characters += string.punctuation

    if not characters:
        messagebox.showerror(
            "Error",
            "Select at least one option."
        )
        return

    length = length_scale.get()

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    password_var.set(password)

    check_strength(password)

# =============================
# Strength Checker
# =============================

def check_strength(password):

    score = 0

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        strength_label.config(
            text="Weak",
            fg="red"
        )

    elif score <= 4:
        strength_label.config(
            text="Medium",
            fg="orange"
        )

    else:
        strength_label.config(
            text="Strong",
            fg="green"
        )

# =============================
# Main Card
# =============================

card = tk.Frame(
    root,
    bg="white",
    padx=30,
    pady=30
)

card.pack(
    padx=30,
    pady=30,
    fill="both",
    expand=True
)

tk.Label(
    card,
    text="Generate Strong Secure Passwords",
    bg="white",
    fg=TEXT,
    font=("Segoe UI", 16, "bold")
).pack(pady=(0,20))

# =============================
# Password Length
# =============================

tk.Label(
    card,
    text="Password Length",
    bg="white",
    font=("Segoe UI", 11, "bold")
).pack(anchor="w")

length_scale = tk.Scale(
    card,
    from_=8,
    to=64,
    orient="horizontal",
    length=450,
    bg="white"
)

length_scale.set(16)
length_scale.pack(pady=10)

# =============================
# Options
# =============================

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    card,
    text="Uppercase (A-Z)",
    variable=upper_var,
    bg="white"
).pack(anchor="w")

tk.Checkbutton(
    card,
    text="Lowercase (a-z)",
    variable=lower_var,
    bg="white"
).pack(anchor="w")

tk.Checkbutton(
    card,
    text="Numbers (0-9)",
    variable=number_var,
    bg="white"
).pack(anchor="w")

tk.Checkbutton(
    card,
    text="Symbols (!@#$)",
    variable=symbol_var,
    bg="white"
).pack(anchor="w")
# =============================
# Generated Password
# =============================

password_var = tk.StringVar()

tk.Label(
    card,
    text="Generated Password",
    bg="white",
    font=("Segoe UI", 11, "bold")
).pack(anchor="w", pady=(20,0))

password_entry = tk.Entry(
    card,
    textvariable=password_var,
    font=("Consolas", 13),
    width=40,
    justify="center"
)

password_entry.pack(pady=10)
tk.Label(
    card,
    text="Strength",
    bg="white",
    font=("Segoe UI", 11, "bold")
).pack()

strength_label = tk.Label(
    card,
    text="-",
    bg="white",
    font=("Segoe UI", 12, "bold")
)

strength_label.pack(pady=5)
tk.Button(
    card,
    text="🎲 Generate Password",
    bg=PRIMARY,
    fg="white",
    width=25,
    command=generate_password
).pack(pady=20)

tk.Button(
    card,
    text="🚀 Use Password",
    bg="blue",
    fg="white",
    width=25,
    command=use_password
).pack(pady=5)

# =============================
# USE PASSWORD BUTTON
# =============================

def use_password():
    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "Warning",
            "Generate a password first."
        )
        return

    # write password to temp file
    with open("/tmp/securevault_password.txt", "w") as f:
        f.write(password)

    # NOW AUTO OPEN Add Password GUI
    import subprocess

    subprocess.Popen([
        "python3",
        "add_password_gui.py"
    ])
# =============================
# Copy Password Function
# =============================

def copy_password():

    password = password_var.get()

    if not password:
        messagebox.showwarning(
            "Warning",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


# =============================
# Buttons Section
# =============================

tk.Button(
    card,
    text="📋 Copy Password",
    bg="gray",
    fg="white",
    width=25,
    command=copy_password
).pack(pady=10)

tk.Button(
    card,
    text="❌ Close",
    bg="red",
    fg="white",
    width=25,
    command=root.destroy
).pack(pady=5)

root.mainloop()
