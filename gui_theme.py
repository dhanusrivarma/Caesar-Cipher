
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from PIL import Image, ImageTk

# Optional import for encryption logic (with fallback if missing)
try:
    from src.cipher import encrypt, decrypt
except ImportError:
    # Fallback Caesar cipher implementation if src.cipher isn't found
    def encrypt(text, shift):
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return "".join(result)

    def decrypt(text, shift):
        return encrypt(text, -shift)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 35
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#FFFFE0",
            foreground="black",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# ---------------- Logic Functions ----------------

def encrypt_text():
    message = input_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message.")
        return
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be a number.")
        return

    result = encrypt(message, shift)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    status.set("✔ Message encrypted successfully")


def decrypt_text():
    message = input_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message.")
        return
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be a number.")
        return

    result = decrypt(message, shift)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    status.set("✔ Message decrypted successfully")


def open_file():
    file_path = filedialog.askopenfilename(
        title="Open Text File",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, content)
            status.set("📂 File loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def save_output():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showerror("Error", "No output to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Output"
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Success", "Output saved successfully!")
            status.set("💾 Output saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def copy_output():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showerror("Error", "No output to copy.")
        return

    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()
    messagebox.showinfo("Copied", "Output copied to clipboard!")
    status.set("📋 Output copied to clipboard")


def show_about():
    messagebox.showinfo(
        "About Caesar Cipher Pro",
        "Caesar Cipher Pro\n\n"
        "Version: 1.0\n\n"
        "Developed in Python using Tkinter.\n\n"
        "Features:\n"
        "• Encrypt Messages\n"
        "• Decrypt Messages\n"
        "• Open Text Files\n"
        "• Save Output\n"
        "• Copy Output\n"
        "• Ancient Roman Wooden GUI"
    )


def clear_fields():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)
    status.set("🧹 Fields cleared")


# ---------------- Main Window Setup ----------------

root = tk.Tk()
root.title("Caesar Cipher Pro")
root.geometry("1024x680")
root.resizable(False, False)

# ---------- Load Background Image ----------
# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "assets", "background.jpg")

if not os.path.exists(bg_path):
    messagebox.showerror(
        "File Error", 
        f"Could not find 'background.jpg'.\n\nLooked in:\n{bg_path}\n\nPlease save the generated background image to that folder!"
    )
    exit()

# --- ADD THESE 4 LINES TO FIX THE "canvas is not defined" ERROR ---
bg_image_raw = Image.open(bg_path)
bg_image_resized = bg_image_raw.resize((1024, 680), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image_resized)

canvas = tk.Canvas(root, width=1024, height=680, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")
# ---------- Menu Bar ----------
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save Output", command=save_output)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copy Output", command=copy_output)
edit_menu.add_command(label="Clear", command=clear_fields)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# ---------------- Overlay UI Components ----------------

# 1. Main Title
canvas.create_text(
    512, 85,
    text="CAESAR CIPHER PRO",
    font=("Cinzel Decorative", 22, "bold"),
    fill="#D4AF37"
)

# 2. Section Labels
canvas.create_text(512, 128, text="ENTER MESSAGE", font=("Georgia", 10, "bold"), fill="#C5A059")
canvas.create_text(512, 258, text="SHIFT VALUE", font=("Georgia", 10, "bold"), fill="#C5A059")
canvas.create_text(512, 458, text="OUTPUT", font=("Georgia", 10, "bold"), fill="#C5A059")

# 3. Input Text Box (Positioned over top parchment)
input_text = tk.Text(
    root,
    height=5,
    width=38,
    font=("Georgia", 11),
    bg="#D8C49F",
    fg="#2A1B0E",
    relief="flat",
    wrap="word",
    insertbackground="#2A1B0E"
)
canvas.create_window(512, 190, window=input_text)

# 4. Shift Entry Box
shift_entry = tk.Entry(
    root,
    font=("Georgia", 12, "bold"),
    width=8,
    bg="#1A110B",
    fg="#FFD700",
    relief="flat",
    justify="center",
    insertbackground="#FFD700"
)
canvas.create_window(485, 285, window=shift_entry)

# 5. Buttons Styling & Alignment
btn_style = {
    "font": ("Georgia", 9, "bold"),
    "bg": "#2A1810",
    "fg": "#D4AF37",
    "activebackground": "#3D2317",
    "activeforeground": "#FFF0A5",
    "relief": "flat",
    "cursor": "hand2"
}

# Row 1
encrypt_button = tk.Button(root, text="ENCRYPT", command=encrypt_text, width=13, **btn_style)
canvas.create_window(435, 328, window=encrypt_button)

decrypt_button = tk.Button(root, text="DECRYPT", command=decrypt_text, width=13, **btn_style)
canvas.create_window(588, 328, window=decrypt_button)

# Row 2
open_button = tk.Button(root, text="OPEN FILE", command=open_file, width=13, **btn_style)
canvas.create_window(435, 362, window=open_button)

save_button = tk.Button(root, text="SAVE OUTPUT", command=save_output, width=13, **btn_style)
canvas.create_window(588, 362, window=save_button)

# Row 3
copy_button = tk.Button(root, text="COPY OUTPUT", command=copy_output, width=13, **btn_style)
canvas.create_window(435, 396, window=copy_button)

clear_button = tk.Button(root, text="CLEAR", command=clear_fields, width=13, **btn_style)
canvas.create_window(588, 396, window=clear_button)

# Row 4
about_button = tk.Button(root, text="ABOUT", command=show_about, width=13, **btn_style)
canvas.create_window(435, 430, window=about_button)

exit_button = tk.Button(root, text="EXIT", command=root.destroy, width=13, **btn_style)
canvas.create_window(588, 430, window=exit_button)

# 6. Output Text Box (Positioned over bottom parchment)
output_text = tk.Text(
    root,
    height=5,
    width=38,
    font=("Georgia", 11),
    bg="#D8C49F",
    fg="#2A1B0E",
    relief="flat",
    wrap="word",
    insertbackground="#2A1B0E"
)
canvas.create_window(512, 520, window=output_text)

# 7. Status Bar
status = tk.StringVar()
status.set("Ready")

status_bar = tk.Label(
    root,
    textvariable=status,
    anchor="w",
    bg="#150E0A",
    fg="#C5A059",
    font=("Georgia", 9),
    padx=10
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ---------------- Tooltips & Keybindings ----------------

ToolTip(encrypt_button, "Encrypt the entered message")
ToolTip(decrypt_button, "Decrypt the entered message")
ToolTip(open_button, "Open a text file")
ToolTip(save_button, "Save output to a text file")
ToolTip(copy_button, "Copy output to clipboard")
ToolTip(clear_button, "Clear all fields")
ToolTip(about_button, "About this application")
ToolTip(exit_button, "Close the application")

root.bind("<Control-e>", lambda event: encrypt_text())
root.bind("<Control-d>", lambda event: decrypt_text())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_output())
root.bind("<Control-l>", lambda event: clear_fields())
root.bind("<Control-q>", lambda event: root.destroy())
root.bind("<F1>", lambda event: show_about())

root.mainloop()