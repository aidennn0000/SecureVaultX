import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import os
import sys
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from theme import *

DB_PATH = os.path.join(BASE_DIR, "database", "vault.db")

# Load encryption key
KEY_PATH = os.path.join(BASE_DIR, "secret.key")

with open(KEY_PATH, "rb") as f:
    key = f.read()

cipher = Fernet(key)

show_passwords = False


# -----------------------------
# Load Vault
# -----------------------------
def load_vault():

    tree.delete(*tree.get_children())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            website,
            username,
            encrypted_password,
            notes
        FROM vault
        ORDER BY website
    """)

    rows = cursor.fetchall()
    conn.close()

    for row in rows:

        id_, website, username, enc_password, notes = row

        try:
            password = cipher.decrypt(enc_password).decode()
        except:
            password = "ERROR"

        display_password = password if show_passwords else "●" * len(password)

        tree.insert(
            "",
            tk.END,
            values=(
                id_,
                website,
                username,
                display_password,
                notes,
                password
            )
        )

    status_label.config(text=f"{len(rows)} password(s) stored")


# -----------------------------
# Search
# -----------------------------
def search(event=None):

    keyword = search_entry.get().lower()

    tree.delete(*tree.get_children())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            website,
            username,
            encrypted_password,
            notes
        FROM vault
    """)

    rows = cursor.fetchall()
    conn.close()

    count = 0

    for row in rows:

        id_, website, username, enc_password, notes = row

        try:
            password = cipher.decrypt(enc_password).decode()
        except:
            password = "ERROR"

        text = f"{website} {username} {notes} {password}".lower()

        if keyword in text:

            display_password = password if show_passwords else "●" * len(password)

            tree.insert(
                "",
                tk.END,
                values=(
                    id_,
                    website,
                    username,
                    display_password,
                    notes,
                    password
                )
            )

            count += 1

    status_label.config(text=f"{count} result(s)")


# -----------------------------
# Toggle Passwords
# -----------------------------
def toggle_passwords():

    global show_passwords

    show_passwords = not show_passwords

    if show_passwords:
        show_btn.config(text="🙈 Hide Passwords")
    else:
        show_btn.config(text="👁 Show Passwords")

    search()


# -----------------------------
# Window
# -----------------------------
root = tk.Tk()

root.title("SecureVaultX Vault")
root.geometry("1200x700")
root.configure(bg=BACKGROUND)

header = tk.Frame(root, bg=PRIMARY, height=60)
header.pack(fill="x")

tk.Label(
    header,
    text="🔐 SecureVaultX Vault",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 18, "bold")
).pack(side="left", padx=20)

content = tk.Frame(root, bg=BACKGROUND)
content.pack(fill="both", expand=True, padx=20, pady=20)

search_frame = tk.Frame(content, bg=BACKGROUND)
search_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    search_frame,
    text="Search",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 11, "bold")
).pack(side="left")

search_entry = tk.Entry(
    search_frame,
    width=40,
    font=("Segoe UI", 11)
)

search_entry.pack(side="left", padx=10)
search_entry.bind("<KeyRelease>", search)

table_frame = tk.Frame(content)
table_frame.pack(fill="both", expand=True)

columns = (
    "ID",
    "Website",
    "Username",
    "Password",
    "Notes",
    "RealPassword"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Website", text="Website")
tree.heading("Username", text="Username")
tree.heading("Password", text="Password")
tree.heading("Notes", text="Notes")

tree.column("ID", width=60)
tree.column("Website", width=220)
tree.column("Username", width=220)
tree.column("Password", width=180)
tree.column("Notes", width=300)

# Hidden column
tree.column("RealPassword", width=0, stretch=False)
tree.heading("RealPassword", text="")
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)


# -----------------------------
# Copy Password
# -----------------------------
def copy_password():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a password."
        )
        return

    values = tree.item(selected)["values"]

    password = values[5]

    root.clipboard_clear()
    root.clipboard_append(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# -----------------------------
# Delete Password
# -----------------------------
def delete_password():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a record."
        )
        return

    values = tree.item(selected)["values"]

    record_id = values[0]

    answer = messagebox.askyesno(
        "Delete",
        "Delete this password?"
    )

    if not answer:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vault WHERE id=?",
        (record_id,)
    )

    conn.commit()
    conn.close()

    load_vault()


# -----------------------------
# Button Area
# -----------------------------
button_frame = tk.Frame(
    content,
    bg=BACKGROUND
)

button_frame.pack(fill="x", pady=15)

show_btn = tk.Button(
    button_frame,
    text="👁 Show Passwords",
    bg=PRIMARY,
    fg="white",
    width=18,
    command=toggle_passwords
)

show_btn.pack(side="left", padx=5)

copy_btn = tk.Button(
    button_frame,
    text="📋 Copy Password",
    width=18,
    command=copy_password
)

copy_btn.pack(side="left", padx=5)

delete_btn = tk.Button(
    button_frame,
    text="🗑 Delete",
    bg=DANGER,
    fg="white",
    width=15,
    command=delete_password
)

delete_btn.pack(side="left", padx=5)

refresh_btn = tk.Button(
    button_frame,
    text="🔄 Refresh",
    width=15,
    command=load_vault
)

refresh_btn.pack(side="left", padx=5)
# -----------------------------
# Back to Dashboard
# -----------------------------
def back_dashboard():

    root.destroy()
    subprocess.Popen(
        ["python3", "dashboard_gui_v2.py"]
    )


dashboard_btn = tk.Button(
    button_frame,
    text="🏠 Dashboard",
    width=18,
    command=back_dashboard
)

dashboard_btn.pack(side="right", padx=5)


# -----------------------------
# Status Bar
# -----------------------------
status_label = tk.Label(
    root,
    text="Loading...",
    bg=BACKGROUND,
    fg="gray",
    anchor="w",
    font=("Segoe UI", 10)
)

status_label.pack(
    fill="x",
    padx=20,
    pady=(0, 10)
)


# -----------------------------
# Style Treeview
# -----------------------------
style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 11, "bold")
)


# -----------------------------
# Start Application
# -----------------------------
load_vault()

root.mainloop()
