import subprocess
import tkinter as tk

root = tk.Tk()
root.title("SecureVaultX")
root.geometry("400x300")

tk.Label(
    root,
    text="SecureVaultX Launcher",
    font=("Arial", 16, "bold")
).pack(pady=20)

def open_login():
    subprocess.Popen(["python3", "gui/login_gui_v2.py"])
    root.destroy()

def open_dashboard():
    subprocess.Popen(["python3", "gui/dashboard_gui_v2.py"])
    root.destroy()

tk.Button(
    root,
    text="🔐 Login",
    width=20,
    command=open_login
).pack(pady=10)

tk.Button(
    root,
    text="📊 Dashboard (Direct)",
    width=20,
    command=open_dashboard
).pack(pady=10)

tk.Button(
    root,
    text="❌ Exit",
    width=20,
    command=root.destroy
).pack(pady=10)

root.mainloop()
