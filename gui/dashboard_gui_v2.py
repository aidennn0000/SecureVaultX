import tkinter as tk
import subprocess
import sqlite3
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from theme import *
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "vault.db")

IDLE_TIME = 300000  # 5 minutes
idle_job = None
# -------------------------
# Get Vault Statistics
# -------------------------
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vault")
    total_passwords = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT website) FROM vault")
    total_websites = cursor.fetchone()[0]

    conn.close()

    return total_passwords, total_websites


# -------------------------
# Open Windows
# -------------------------
def open_add():
    subprocess.Popen(["python3", "gui/add_password_gui_v2.py"])


def open_vault():
    subprocess.Popen(["python3", "gui/view_vault_gui_v2.py"])


def logout():
    root.destroy()
    subprocess.Popen(["python3", "gui/login_gui_v2.py"])

def auto_lock():
    global idle_job

    idle_job = None

    root.destroy()
    subprocess.Popen(["python3", "gui/login_gui_v2.py"])

def reset_timer(event=None):
    global idle_job

    if idle_job:
        root.after_cancel(idle_job)

    idle_job = root.after(
        IDLE_TIME,
        auto_lock
    )

# -------------------------
# Logged-in User
# -------------------------
username = "User"

if len(sys.argv) > 1:
    username = sys.argv[1]

passwords, websites = get_stats()

# -------------------------
# Window
# -------------------------
root = tk.Tk()
root.title("SecureVaultX Dashboard")
root.geometry("1000x650")
root.configure(bg=BACKGROUND)
root.resizable(False, False)

# -------------------------
# Header
# -------------------------
header = tk.Frame(root, bg=PRIMARY, height=70)
header.pack(fill="x")

tk.Label(
    header,
    text="🔐 SecureVaultX",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(side="left", padx=20, pady=15)

tk.Label(
    header,
    text=f"Welcome, {username}",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 12)
).pack(side="right", padx=20)

# -------------------------
# Main Area
# -------------------------
main = tk.Frame(root, bg=BACKGROUND)
main.pack(fill="both", expand=True, padx=20, pady=20)

# -------------------------
# Card Function
# -------------------------
def make_card(parent, title, value):
    frame = tk.Frame(
        parent,
        bg="white",
        width=220,
        height=120,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(side="left", padx=10)
    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        bg="white",
        fg=SECONDARY_TEXT,
        font=("Segoe UI", 11)
    ).pack(pady=(15, 5))

    tk.Label(
        frame,
        text=str(value),
        bg="white",
        fg=TEXT,
        font=("Segoe UI", 24, "bold")
    ).pack()

    return frame

cards = tk.Frame(main, bg=BACKGROUND)
cards.pack()

make_card(cards, "Passwords", passwords)
make_card(cards, "Websites", websites)
make_card(cards, "Security", "Strong")

# -------------------------
# Quick Actions
# -------------------------
actions = tk.Frame(main, bg=BACKGROUND)
actions.pack(pady=40)

tk.Label(
    actions,
    text="Quick Actions",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 16, "bold")
).pack(pady=10)

tk.Button(
    actions,
    text="➕ Add Password",
    bg=PRIMARY,
    fg="white",
    width=25,
    font=("Segoe UI", 11, "bold"),
    command=open_add
).pack(pady=8)

tk.Button(
    actions,
    text="📂 View Vault",
    bg=PRIMARY,
    fg="white",
    width=25,
    font=("Segoe UI", 11, "bold"),
    command=open_vault
).pack(pady=8)

tk.Button(
    actions,
    text="🚪 Logout",
    bg=DANGER,
    fg="white",
    width=25,
    font=("Segoe UI", 11, "bold"),
    command=logout
).pack(pady=8)

# -------------------------
# Footer
# -------------------------
tk.Label(
    root,
    text="SecureVaultX © 2026 | Encrypted Password Manager",
    bg=BACKGROUND,
    fg=SECONDARY_TEXT,
    font=("Segoe UI", 10)
).pack(side="bottom", pady=15)

root.bind_all("<Key>", reset_timer)
root.bind_all("<Motion>", reset_timer)
root.bind_all("<Button>", reset_timer)

reset_timer()
root.mainloop()
