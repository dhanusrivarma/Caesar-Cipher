import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import hashlib

PASSWORD_HASH = "dec17192017ffdf7fca5445d4ca295a57640c8b0c89333acaaa5f7a50e50a599"

def login():

    entered_password = password_entry.get()

    entered_hash = hashlib.sha256(
        entered_password.encode()
    ).hexdigest()

    if entered_hash == PASSWORD_HASH:

        root.destroy()

        subprocess.Popen([sys.executable, "gui.py"])

    else:

        messagebox.showerror(
            "Error",
            "Incorrect password!"
        )


root = tk.Tk()

root.title("Login")
root.geometry("500x280")
root.resizable(False, False)

tk.Label(
    root,
    text="Caesar Cipher Pro",
    font=("Segoe UI", 16, "bold")
).pack(pady=10)

tk.Label(
    root,
    text="Password"
).pack()

password_frame = tk.Frame(root)
password_frame.pack(pady=5)

password_entry = tk.Entry(
    password_frame,
    show="*",
    width=30
)
password_entry.pack(side="left")
password_entry.focus()

show_password = False


def toggle_password():
    global show_password

    show_password = not show_password

    if show_password:
        password_entry.config(show="")
        toggle_btn.config(text="🙈")
    else:
        password_entry.config(show="*")
        toggle_btn.config(text="👁")


toggle_btn = tk.Button(
    password_frame,
    text="👁",
    command=toggle_password,
    width=3
)
toggle_btn.pack(side="left", padx=5)

login_button = tk.Button(
    root,
    text="Login",
    width=15,
    command=login
)
login_button.pack(pady=20, padx=(0, 25))

root.bind("<Return>", lambda event: login())

root.mainloop()