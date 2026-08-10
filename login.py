import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import hashlib
import json
import os


# ============================================================
# SETTINGS
# ============================================================

USERS_FILE = "users.json"

BG_COLOR = "#EEF2FF"
CARD_COLOR = "#FFFFFF"
PRIMARY = "#5B2EFF"
SECONDARY = "#2878F0"
TEXT_COLOR = "#172033"
MUTED = "#667085"
BORDER = "#D9DDF0"


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():

    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users(users):

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


# ============================================================
# OPEN MAIN APPLICATION
# ============================================================


def open_cipher_app(username):
    root.destroy()

    subprocess.Popen([
        sys.executable,
        "gui.py",
        username
    ])

# ============================================================
# LOGIN
# ============================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:

        messagebox.showerror(
            "Login Error",
            "Please enter username and password."
        )

        return

    users = load_users()

    entered_hash = hash_password(password)

    if username in users and users[username] == entered_hash:

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {username}! 🎉"
        )

        open_cipher_app(username)

    else:

        messagebox.showerror(
            "Login Failed",
            "Incorrect username or password."
        )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

show_password = False


def toggle_password():

    global show_password

    show_password = not show_password

    if show_password:

        password_entry.config(show="")
        toggle_button.config(text="🙈")

    else:

        password_entry.config(show="*")
        toggle_button.config(text="👁")


# ============================================================
# CREATE ACCOUNT
# ============================================================

def open_register():

    register_window = tk.Toplevel(root)

    register_window.title("Create Account")
    register_window.geometry("500x620")
    register_window.resizable(False, False)

    register_window.configure(
        bg=BG_COLOR
    )

    register_window.transient(root)
    register_window.grab_set()


    # ========================================================
    # REGISTER HEADER
    # ========================================================

    tk.Label(
        register_window,
        text="🔐",
        font=("Segoe UI", 28),
        bg=BG_COLOR
    ).pack(
        pady=(18, 2)
    )


    tk.Label(
        register_window,
        text="Create Your Account",
        font=("Segoe UI", 19, "bold"),
        fg=PRIMARY,
        bg=BG_COLOR
    ).pack()


    tk.Label(
        register_window,
        text="Create your own secure login",
        font=("Segoe UI", 10),
        fg=MUTED,
        bg=BG_COLOR
    ).pack(
        pady=(4, 18)
    )


    # ========================================================
    # REGISTER CARD
    # ========================================================

    card = tk.Frame(
        register_window,
        bg=CARD_COLOR,
        padx=30,
        pady=22,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        padx=35,
        pady=5
    )


    # ========================================================
    # USERNAME
    # ========================================================

    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(
        anchor="w"
    )


    register_username = tk.Entry(
        card,
        font=("Segoe UI", 10),
        width=38,
        relief="solid",
        bd=1
    )

    register_username.pack(
        ipady=5,
        pady=(5, 13)
    )


    # ========================================================
    # PASSWORD
    # ========================================================

    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(
        anchor="w"
    )


    register_password = tk.Entry(
        card,
        font=("Segoe UI", 10),
        width=38,
        show="*",
        relief="solid",
        bd=1
    )

    register_password.pack(
        ipady=5,
        pady=(5, 13)
    )


    # ========================================================
    # CONFIRM PASSWORD
    # ========================================================

    tk.Label(
        card,
        text="Confirm Password",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT_COLOR,
        bg=CARD_COLOR
    ).pack(
        anchor="w"
    )


    register_confirm = tk.Entry(
        card,
        font=("Segoe UI", 10),
        width=38,
        show="*",
        relief="solid",
        bd=1
    )

    register_confirm.pack(
        ipady=5,
        pady=(5, 8)
    )


    tk.Label(
        card,
        text="Password must contain at least 6 characters.",
        font=("Segoe UI", 8),
        fg=MUTED,
        bg=CARD_COLOR
    ).pack(
        anchor="w"
    )


    # ========================================================
    # CREATE ACCOUNT FUNCTION
    # ========================================================

    def create_account():

        username = register_username.get().strip()
        password = register_password.get()
        confirm_password = register_confirm.get()


        if not username or not password or not confirm_password:

            messagebox.showerror(
                "Error",
                "Please fill in all fields.",
                parent=register_window
            )

            return


        if len(password) < 6:

            messagebox.showerror(
                "Error",
                "Password must contain at least 6 characters.",
                parent=register_window
            )

            return


        if password != confirm_password:

            messagebox.showerror(
                "Error",
                "Passwords do not match.",
                parent=register_window
            )

            return


        users = load_users()


        if username in users:

            messagebox.showerror(
                "Error",
                "Username already exists.",
                parent=register_window
            )

            return


        # Save HASHED password
        users[username] = hash_password(password)

        save_users(users)


        # Close registration window
        register_window.destroy()


        # Welcome the new user
        messagebox.showinfo(
            "Welcome!",
            f"Account created successfully!\n\n"
            f"Welcome, {username}! 🎉",
            parent=root
        )


        # Automatically open Caesar Cipher Pro
        open_cipher_app(username)


    # ========================================================
    # CREATE ACCOUNT BUTTON
    # ========================================================

    create_account_button = tk.Button(
        card,
        text="✓  Create Account",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=PRIMARY,
        activebackground=SECONDARY,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=32,
        command=create_account
    )

    create_account_button.pack(
        ipady=6,
        pady=(18, 0)
    )


    # Press Enter to create account
    register_window.bind(
        "<Return>",
        lambda event: create_account()
    )

    register_username.focus()


# ============================================================
# MAIN LOGIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Caesar Cipher Pro - Login")
root.geometry("560x650")
root.resizable(False, False)

root.configure(
    bg=BG_COLOR
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=PRIMARY,
    height=125
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


tk.Label(
    header,
    text="🔐",
    font=("Segoe UI", 30),
    bg=PRIMARY,
    fg="white"
).pack(
    pady=(14, 0)
)


tk.Label(
    header,
    text="CAESAR CIPHER PRO",
    font=("Segoe UI", 18, "bold"),
    bg=PRIMARY,
    fg="white"
).pack()


# ============================================================
# LOGIN CARD
# ============================================================

card = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=38,
    pady=25,
    highlightbackground=BORDER,
    highlightthickness=1
)

card.pack(
    padx=50,
    pady=25
)


# ============================================================
# WELCOME
# ============================================================

tk.Label(
    card,
    text="Welcome Back!",
    font=("Segoe UI", 20, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
).pack(
    pady=(0, 4)
)


tk.Label(
    card,
    text="Secure Encryption & Decryption Tool",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD_COLOR
).pack(
    pady=(0, 22)
)


# ============================================================
# USERNAME LABEL
# ============================================================

tk.Label(
    card,
    text="👤  Username",
    font=("Segoe UI", 10, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
).pack(
    anchor="w"
)


# ============================================================
# USERNAME ENTRY
# ============================================================

username_entry = tk.Entry(
    card,
    font=("Segoe UI", 10),
    width=45,
    relief="solid",
    bd=1
)

username_entry.pack(
    ipady=6,
    pady=(5, 16)
)


# ============================================================
# PASSWORD LABEL
# ============================================================

tk.Label(
    card,
    text="🔒  Password",
    font=("Segoe UI", 10, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
).pack(
    anchor="w"
)


# ============================================================
# PASSWORD FRAME
# ============================================================

password_frame = tk.Frame(
    card,
    bg=CARD_COLOR
)

password_frame.pack(
    pady=(5, 5)
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 10),
    width=38,
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(
    side="left",
    ipady=6
)


# ============================================================
# EYE BUTTON
# ============================================================

toggle_button = tk.Button(
    password_frame,
    text="👁",
    font=("Segoe UI", 10),
    fg=PRIMARY,
    bg=CARD_COLOR,
    activebackground=BG_COLOR,
    activeforeground=PRIMARY,
    relief="solid",
    bd=1,
    width=3,
    cursor="hand2",
    command=toggle_password
)

toggle_button.pack(
    side="left",
    padx=(6, 0),
    ipady=3
)


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = tk.Button(
    card,
    text="🔐  Login",
    font=("Segoe UI", 11, "bold"),
    fg="white",
    bg=PRIMARY,
    activebackground=SECONDARY,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=38,
    command=login
)

login_button.pack(
    ipady=7,
    pady=(20, 12)
)


# ============================================================
# DIVIDER
# ============================================================

tk.Frame(
    card,
    bg=BORDER,
    height=1,
    width=400
).pack(
    pady=5
)


# ============================================================
# CREATE ACCOUNT TEXT
# ============================================================

tk.Label(
    card,
    text="New to Caesar Cipher Pro?",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD_COLOR
).pack(
    pady=(10, 7)
)


# ============================================================
# CREATE NEW ACCOUNT BUTTON
# ============================================================

register_button = tk.Button(
    card,
    text="👤  Create New Account",
    font=("Segoe UI", 10, "bold"),
    fg=PRIMARY,
    bg=CARD_COLOR,
    activebackground=BG_COLOR,
    activeforeground=SECONDARY,
    relief="solid",
    bd=1,
    cursor="hand2",
    width=38,
    command=open_register
)

register_button.pack(
    ipady=6
)


# ============================================================
# FOOTER
# ============================================================

tk.Label(
    root,
    text="🔒 Your password is securely hashed",
    font=("Segoe UI", 8),
    fg=MUTED,
    bg=BG_COLOR
).pack(
    pady=(0, 10)
)


# ============================================================
# ENTER KEY
# ============================================================

root.bind(
    "<Return>",
    lambda event: login()
)


username_entry.focus()


# ============================================================
# START
# ============================================================

root.mainloop()