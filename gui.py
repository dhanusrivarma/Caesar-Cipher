import tkinter as tk
from tkinter import messagebox, filedialog
import json
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from src.cipher import encrypt, decrypt

# ---------------- History ----------------

history = []


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

def update_counter(event=None):

    text = input_text.get("1.0", "end-1c")

    characters = len(text)

    words = len(text.split())

    lines = len(text.splitlines())

    counter.set(
        f"Characters: {characters}    "
        f"Words: {words}    "
        f"Lines: {lines}"
    )

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

    history.append({
    "Operation": "Encrypt",
    "Shift": shift,
    "Input": message,
    "Output": result,
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

    print(history)

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

    history.append({
    "Operation": "Decrypt",
    "Shift": shift,
    "Input": message,
    "Output": result,
    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})
    print(history)

    status.set("✔ Message decrypted successfully")

def open_file():
    file_path = filedialog.askopenfilename(
        title="Open Text File",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()

            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, content)

            update_status("📂 File loaded successfully")

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
            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo(
                "Success",
                "Output saved successfully!"
            )

            update_status("💾 Output saved successfully")

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

    messagebox.showinfo(
        "Copied",
        "Output copied to clipboard!"
    )

    update_status("📋 Output copied to clipboard")


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
        "• User-Friendly GUI"
    )

def exit_program():
    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()

def clear_fields():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)

    update_status("🧹 Fields cleared")

def reset_status():
    status.set("Ready")


def update_status(message):
    status.set(message)

    root.after(
        3000,
        reset_status
    )

def show_history():

    if not history:
        messagebox.showinfo(
            "History",
            "No history available."
        )
        return

    history_window = tk.Toplevel(root)
    history_window.title("Encryption History")
    history_window.geometry("700x500")

    text = tk.Text(
        history_window,
        wrap="word",
        font=("Consolas", 10)
    )

    text.pack(
        fill="both",
        expand=True
    )

    for item in history:

     text.insert(
    tk.END,
    f"========== {item['Operation'].upper()} ==========\n"
    f"Time  : {item['Time']}\n"
    f"Shift : {item['Shift']}\n"
    f"Input : {item['Input']}\n"
    f"Output: {item['Output']}\n\n"
)

    text.config(state="disabled")

def clear_history():

    if not history:
        messagebox.showinfo(
            "History",
            "History is already empty."
        )
        return

    answer = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to clear all history?"
    )

    if answer:
        history.clear()

        messagebox.showinfo(
            "History",
            "History cleared successfully."
        )

        update_status("🗑 History cleared")


def export_history_pdf():

    if not history:
        messagebox.showinfo(
            "History",
            "No history available to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save History as PDF"
    )

    if not file_path:
        return

    try:

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Caesar Cipher Pro - History Report</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        for item in history:

            text = (
    f"<b>{item['Operation']}</b><br/>"
    f"Time : {item['Time']}<br/>"
    f"Shift : {item['Shift']}<br/>"
    f"Input : {item['Input']}<br/>"
    f"Output : {item['Output']}<br/><br/>"
)

            story.append(
                Paragraph(
                    text,
                    styles["BodyText"]
                )
            )

        doc.build(story)

        messagebox.showinfo(
            "Success",
            "History exported successfully!"
        )

        update_status("📄 History exported as PDF")

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e))

def export_history_json():

    if not history:
        messagebox.showinfo(
            "History",
            "No history available to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")],
        title="Save History as JSON"
    )

    if not file_path:
        return

    try:

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(
                history,
                file,
                indent=4
            )

        messagebox.showinfo(
            "Success",
            "History exported successfully!"
        )

        update_status("📄 History exported as JSON")

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def import_history_json():

    global history

    file_path = filedialog.askopenfilename(
        title="Import History",
        filetypes=[("JSON Files", "*.json")]
    )

    if not file_path:
        return

    try:

        with open(file_path, "r", encoding="utf-8") as file:
            history = json.load(file)

        messagebox.showinfo(
            "Success",
            "History imported successfully!"
        )

        update_status("📂 History imported")

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

# ---------------- Main Window ----------------

root = tk.Tk()
root.title("Caesar Cipher Pro")
root.geometry("600x600")
root.configure(bg="#EAF4FC")

# ---------------- Menu Bar ----------------

menu_bar = tk.Menu(root)

# ---------- File Menu ----------

file_menu = tk.Menu(menu_bar, tearoff=0)

file_menu.add_command(
    label="Open File",
    command=open_file
)

file_menu.add_command(
    label="Save Output",
    command=save_output
)

file_menu.add_separator()

file_menu.add_command(
    label="Exit",
    command=exit_program
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)

# ---------- Edit Menu ----------

edit_menu = tk.Menu(menu_bar, tearoff=0)

edit_menu.add_command(
    label="Copy Output",
    command=copy_output
)

edit_menu.add_command(
    label="Clear",
    command=clear_fields
)

menu_bar.add_cascade(
    label="Edit",
    menu=edit_menu
)

# ---------- Help Menu ----------

help_menu = tk.Menu(menu_bar, tearoff=0)

help_menu.add_command(
    label="About",
    command=show_about
)

menu_bar.add_cascade(
    label="Help",
    menu=help_menu)

# ---------- History Menu ---------- 
history_menu = tk.Menu(menu_bar, tearoff=0)

history_menu.add_command(
    label="View History",
    command=show_history
)

history_menu.add_command(
    label="Export History as PDF",
    command=export_history_pdf
)

history_menu.add_command(
    label="Export History as JSON",
    command=export_history_json
)

history_menu.add_command(
    label="Import History from JSON",
    command=import_history_json
)

history_menu.add_separator()

history_menu.add_command(
    label="Clear History",
    command=clear_history
)

menu_bar.add_cascade(
    label="History",
    menu=history_menu
)

root.config(menu=menu_bar)

# ---------------- Status Variable ----------------

status = tk.StringVar()
status.set("Ready")

# ---------------- Title ----------------

title = tk.Label(
    root,
    text="Caesar Cipher Pro",
    font=("Segoe UI", 22, "bold"),
    fg="#1565C0",
    bg="#EAF4FC"
)
title.pack(pady=10)

# ---------------- Input Label ----------------

tk.Label(
    root,
    text="Enter Message",
    font=("Segoe UI", 10, "bold"),
    fg="#0D47A1",
    bg="#EAF4FC"
).pack()

# ---------------- Input Box ----------------

input_text = tk.Text(
    root,
    height=6,
    width=60,
    font=("Segoe UI", 10)
)
input_text.pack()

# ---------------- Shift ----------------

tk.Label(
    root,
    text="Shift Value",
    font=("Segoe UI", 10, "bold"),
    fg="#0D47A1",
    bg="#EAF4FC"
).pack(pady=5)

shift_entry = tk.Entry(
    root,
    font=("Segoe UI", 10)
)
shift_entry.pack()

# ---------------- Button Frame ----------------

button_frame = tk.Frame(root, bg="#EAF4FC")
button_frame.pack(pady=15)

button_style = {
    "width": 15,
    "bg": "#1976D2",
    "fg": "white",
    "font": ("Segoe UI", 10, "bold"),
    "activebackground": "#1565C0",
    "activeforeground": "white",
    "cursor": "hand2"
}

# Encrypt
encrypt_button = tk.Button(
    button_frame,
    text="🔒 Encrypt",
    command=encrypt_text,
    **button_style
)
encrypt_button.grid(row=0, column=0, padx=5, pady=5)

# Decrypt
decrypt_button = tk.Button(
    button_frame,
    text="🔓 Decrypt",
    command=decrypt_text,
    **button_style
)
decrypt_button.grid(row=0, column=1, padx=5, pady=5)

# Open File
open_button = tk.Button(
    button_frame,
    text="📂 Open File",
    command=open_file,
    **button_style
)
open_button.grid(row=1, column=0, padx=5, pady=5)

# Save Output
save_button = tk.Button(
    button_frame,
    text="💾 Save Output",
    command=save_output,
    **button_style
)
save_button.grid(row=1, column=1, padx=5, pady=5)

# Copy Output
copy_button = tk.Button(
    button_frame,
    text="📋 Copy Output",
    command=copy_output,
    **button_style
)
copy_button.grid(row=2, column=0, padx=5, pady=5)

# Clear
clear_button = tk.Button(
    button_frame,
    text="🧹 Clear",
    command=clear_fields,
    **button_style
)
clear_button.grid(row=2, column=1, padx=5, pady=5)

# About
about_button = tk.Button(
    button_frame,
    text="ℹ️ About",
    command=show_about,
    **button_style
)
about_button.grid(row=3, column=0, padx=5, pady=5)

# Exit
exit_button = tk.Button(
    button_frame,
    text="❌ Exit",
    command=exit_program,
    **button_style
)
exit_button.grid(row=3, column=1, padx=5, pady=5)

# ---------------- Output ----------------

tk.Label(
    root,
    text="Output",
    font=("Segoe UI", 10, "bold"),
    fg="#0D47A1",
    bg="#EAF4FC"
).pack()

output_text = tk.Text(
    root,
    height=6,
    width=60,
    font=("Segoe UI", 10)
)
output_text.pack()

# ---------------- Live Counter ----------------

counter = tk.StringVar()

counter.set(
    "Characters: 0    Words: 0    Lines: 0"
)

# ---------------- Status Bar ----------------

counter_label = tk.Label(
    root,
    textvariable=counter,
    bg="#EAF4FC",
    fg="#1565C0",
    font=("Segoe UI", 9, "bold")
)

counter_label.pack(
    pady=5
)
status_bar = tk.Label(
    root,
    textvariable=status,
    bd=1,
    relief=tk.SUNKEN,
    anchor="w",
    bg="#D6EAF8",
    fg="#0D47A1",
    font=("Segoe UI", 9)
)

status_bar.pack(side=tk.BOTTOM, fill=tk.X)


# ---------------- Keyboard Shortcuts ----------------
input_text.bind(
    "<KeyRelease>",
    update_counter
)
root.bind("<Control-e>", lambda event: encrypt_text())
root.bind("<Control-d>", lambda event: decrypt_text())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_output())
root.bind("<Control-l>", lambda event: clear_fields())
root.bind("<Control-q>", lambda event: exit_program())
root.bind("<F1>", lambda event: show_about())

ToolTip(
    encrypt_button,
    "Encrypt the entered message"
)

ToolTip(
    decrypt_button,
    "Decrypt the entered message"
)

ToolTip(
    open_button,
    "Open a text file"
)

ToolTip(
    save_button,
    "Save output to a text file"
)

ToolTip(
    copy_button,
    "Copy output to clipboard"
)

ToolTip(
    clear_button,
    "Clear all fields"
)

ToolTip(
    about_button,
    "About this application"
)

ToolTip(
    exit_button,
    "Close the application"
)

root.protocol("WM_DELETE_WINDOW", exit_program)

root.mainloop()