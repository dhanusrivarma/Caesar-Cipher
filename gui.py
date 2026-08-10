import tkinter as tk
from tkinter import messagebox, filedialog
import json
import time
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from src.cipher import encrypt, decrypt, atbash, rail_fence_encrypt
from src.vigenere import encrypt_vigenere, decrypt_vigenere

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

def update_cipher(*args):

    selected_cipher = cipher_var.get()

    # Hide the key widgets first
    key_label.pack_forget()
    key_entry.pack_forget()

    if selected_cipher == "Caesar":

        key_label.config(text="Shift Value")

        key_label.pack(
            before=button_frame,
            pady=5
        )

        key_entry.pack(
            before=button_frame
        )

    elif selected_cipher == "Vigenère":

        key_label.config(text="Keyword")

        key_label.pack(
            before=button_frame,
            pady=5
        )

        key_entry.pack(
            before=button_frame
        )

    elif selected_cipher == "ROT13":

        # No key required
        pass

    elif selected_cipher == "Atbash":

        # No key required
        pass

    elif selected_cipher == "Rail Fence":

        key_label.config(text="Rails")

        key_label.pack(
            before=button_frame,
            pady=5
        )

        key_entry.pack(
            before=button_frame
        )


def rot13(text):
    result = ""

    for char in text:
        if "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + 13) % 26 + ord("A"))

        elif "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + 13) % 26 + ord("a"))

        else:
            result += char

    return result


# ---------------- Rail Fence Encrypt ----------------

def rail_fence_encrypt(text, rails):

    if rails <= 1:
        return text

    fence = [[] for _ in range(rails)]

    row = 0
    direction = 1

    for char in text:

        fence[row].append(char)

        if row == 0:
            direction = 1

        elif row == rails - 1:
            direction = -1

        row += direction

    result = ""

    for rail in fence:
        result += "".join(rail)

    return result


# ---------------- Rail Fence Decrypt ----------------

def rail_fence_decrypt(ciphertext, rails):

    if rails <= 1:
        return ciphertext

    pattern = []

    row = 0
    direction = 1

    for _ in range(len(ciphertext)):

        pattern.append(row)

        if row == 0:
            direction = 1

        elif row == rails - 1:
            direction = -1

        row += direction

    rail_counts = [0] * rails

    for r in pattern:
        rail_counts[r] += 1

    rails_data = []

    index = 0

    for count in rail_counts:

        rails_data.append(
            list(ciphertext[index:index + count])
        )

        index += count

    result = []

    rail_positions = [0] * rails

    for r in pattern:

        result.append(
            rails_data[r][rail_positions[r]]
        )

        rail_positions[r] += 1

    return "".join(result)

def encrypt_text():

    message = input_text.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror(
            "Error",
            "Please enter a message."
        )
        return

    # ---------------- Caesar ----------------
    if cipher_var.get() == "Caesar":

        try:
            shift = int(key_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Shift must be a number."
            )
            return

        result = encrypt(message, shift)
        key_value = shift

    # ---------------- Vigenère ----------------
    elif cipher_var.get() == "Vigenère":

        key = key_entry.get().strip()

        if not key:
            messagebox.showerror(
                "Error",
                "Please enter a Vigenère keyword."
            )
            return

        if not key.isalpha():
            messagebox.showerror(
                "Error",
                "Vigenère keyword must contain letters only."
            )
            return

        result = encrypt_vigenere(
            message,
            key
        )

        key_value = key

    # ---------------- ROT13 ----------------
    elif cipher_var.get() == "ROT13":

        result = rot13(message)

        key_value = "None"

    # ---------------- Atbash ----------------
    elif cipher_var.get() == "Atbash":

        result = atbash(message)

        key_value = "None"

    # ---------------- Rail Fence ----------------
    elif cipher_var.get() == "Rail Fence":

        try:
            rails = int(key_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Rails must be a number."
            )
            return

        if rails < 2:
            messagebox.showerror(
                "Error",
                "Rails must be 2 or greater."
            )
            return

        result = rail_fence_encrypt(
            message,
            rails
        )

        key_value = rails

    # ---------------- Output ----------------
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", str(result))

    # ---------------- History ----------------
    history.append({
        "Operation": "Encrypt",
        "Cipher": cipher_var.get(),
        "Key": key_value,
        "Input": message,
        "Output": result,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_history()

    print(history)

    status.set("✔ Message encrypted successfully")

def decrypt_text():

    message = input_text.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror(
            "Error",
            "Please enter a message."
        )
        return

    # ---------------- Caesar ----------------
    if cipher_var.get() == "Caesar":

        try:
            shift = int(key_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Shift must be a number."
            )
            return

        result = decrypt(message, shift)
        key_value = shift

    # ---------------- Vigenère ----------------
    elif cipher_var.get() == "Vigenère":

        key = key_entry.get().strip()

        if not key:
            messagebox.showerror(
                "Error",
                "Please enter a Vigenère keyword."
            )
            return

        if not key.isalpha():
            messagebox.showerror(
                "Error",
                "Vigenère keyword must contain letters only."
            )
            return

        result = decrypt_vigenere(
            message,
            key
        )

        key_value = key

    # ---------------- ROT13 ----------------
    elif cipher_var.get() == "ROT13":

        result = rot13(message)
        key_value = "None"

    # ---------------- Atbash ----------------
    elif cipher_var.get() == "Atbash":

        result = atbash(message)
        key_value = "None"

    # ---------------- Rail Fence ----------------
    elif cipher_var.get() == "Rail Fence":

        try:
            rails = int(key_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Rails must be a number."
            )
            return

        if rails < 2:
            messagebox.showerror(
                "Error",
                "Rails must be 2 or greater."
            )
            return

        result = rail_fence_decrypt(
            message,
            rails
        )

        key_value = rails

    # ---------------- Output ----------------
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", str(result))

    # ---------------- History ----------------
    history.append({
        "Operation": "Decrypt",
        "Cipher": cipher_var.get(),
        "Key": key_value,
        "Input": message,
        "Output": result,
        "Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    save_history()

    print(history)

    status.set(
        "✔ Message decrypted successfully"
    )

def brute_force():

    message = input_text.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror(
            "Error",
            "Please enter encrypted text."
        )
        return

    window = tk.Toplevel(root)
    window.title("Caesar Cipher Cracker")
    window.geometry("700x550")

    text = tk.Text(
        window,
        font=("Consolas", 11),
        wrap="word"
    )

    text.pack(fill="both", expand=True)

    for shift in range(26):

        result = decrypt(message, shift)

        text.insert(
            tk.END,
            f"Shift {shift}\n"
            f"{result}\n\n"
            f"{'-'*45}\n\n"
        )

    text.config(state="disabled")

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

def change_password():

    change_window = tk.Toplevel(root)
    change_window.title("Change Password")
    change_window.geometry("350x250")
    change_window.resizable(False, False)

    tk.Label(
        change_window,
        text="Current Password"
    ).pack(pady=5)

    current_entry = tk.Entry(
        change_window,
        show="*",
        width=30
    )
    current_entry.pack()

    tk.Label(
        change_window,
        text="New Password"
    ).pack(pady=5)

    new_entry = tk.Entry(
        change_window,
        show="*",
        width=30
    )
    new_entry.pack()

    tk.Label(
        change_window,
        text="Confirm Password"
    ).pack(pady=5)

    confirm_entry = tk.Entry(
        change_window,
        show="*",
        width=30
    )
    confirm_entry.pack()

    def save_password():

        with open("password.txt", "r") as file:
            current_password = file.read().strip()

        if current_entry.get() != current_password:
            messagebox.showerror(
                "Error",
                "Current password is incorrect."
            )
            return

        if new_entry.get() != confirm_entry.get():
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
            return

        if new_entry.get().strip() == "":
            messagebox.showerror(
                "Error",
                "New password cannot be empty."
            )
            return

        with open("password.txt", "w") as file:
            file.write(new_entry.get())

        messagebox.showinfo(
            "Success",
            "Password changed successfully!"
        )

        change_window.destroy()

    tk.Button(
        change_window,
        text="Change Password",
        command=save_password,
        width=18
    ).pack(pady=15)

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
    key_entry.delete(0, tk.END)

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
    f"Cipher : {item.get('Cipher', 'Caesar')}\n"
    f"Key    : {item.get('Key', item.get('Shift', 'None'))}\n"
    f"Input : {item['Input']}\n"
    f"Output: {item['Output']}\n\n"
)

    text.config(state="disabled")

def search_history():

    if not history:
        messagebox.showinfo(
            "History",
            "No history available."
        )
        return

    search_window = tk.Toplevel(root)
    search_window.title("Search History")
    search_window.geometry("700x500")

    tk.Label(
        search_window,
        text="🔍 Search:",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=5)

    search_entry = tk.Entry(
        search_window,
        width=45,
        font=("Segoe UI", 11)
    )
    search_entry.pack(pady=5)

    result_box = tk.Text(
        search_window,
        wrap="word",
        font=("Consolas", 10)
    )
    result_box.pack(fill="both", expand=True)

    def update_results(event=None):

        keyword = search_entry.get().lower()

        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        found = False

        for item in history:

            text = (
                f"{item['Operation']} "
                f"{item['Input']} "
                f"{item['Output']}"
            ).lower()

            if keyword in text:

                found = True

                result_box.insert(
                    tk.END,
                    f"========== {item['Operation'].upper()} ==========\n"
                    f"Time   : {item['Time']}\n"
                    f"Cipher : {item.get('Cipher', 'Caesar')}\n"
                    f"Key    : {item.get('Key', item.get('Shift', 'None'))}\n"
                    f"Input  : {item['Input']}\n"
                    f"Output : {item['Output']}\n\n"
                )

        if not found:
            result_box.insert(
                tk.END,
                "No matching history found."
            )

        result_box.config(state="disabled")

    search_entry.bind("<KeyRelease>", update_results)

    update_results()

    
    def perform_search():

        print("Search button clicked")

        keyword = search_entry.get().lower()

        print("Searching:", keyword)
        print("History:", history)


        result_box.delete("1.0", tk.END)

        found = False

        for item in history:

            text = (
                f"{item['Operation']} "
                f"{item['Input']} "
                f"{item['Output']}"
            ).lower()

            if keyword in text:

                found = True

                result_box.insert(
                    tk.END,
                    f"========== {item['Operation'].upper()} ==========\n"
                    f"Time   : {item['Time']}\n"
                    f"Cipher : {item.get('Cipher', 'Caesar')}\n"
                    f"Key    : {item.get('Key', item.get('Shift', 'None'))}\n"
                    f"Input : {item['Input']}\n"
                    f"Output: {item['Output']}\n\n"
                )

        if not found:

            result_box.insert(
                tk.END,
                "No matching history found."
            )


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

        save_history()

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

def save_history():

    try:

        with open("history.json", "w", encoding="utf-8") as file:

            json.dump(
                history,
                file,
                indent=4
            )

    except:
        pass

def load_history():

    global history

    try:

        with open("history.json", "r", encoding="utf-8") as file:

            history = json.load(file)

    except:

        history = []

def show_statistics():

    if not history:
        messagebox.showinfo(
            "Statistics",
            "No history available."
        )
        return

    total = len(history)

    encrypt_count = 0
    decrypt_count = 0

    total_characters = 0
    shifts = []

    for item in history:

        if item["Operation"] == "Encrypt":
            encrypt_count += 1
        else:
            decrypt_count += 1

        total_characters += len(item["Input"])

        shifts.append(item["Shift"])

    average_shift = sum(shifts) / len(shifts)

    most_used_shift = max(
        set(shifts),
        key=shifts.count
    )

    messagebox.showinfo(
        "Statistics",

        f"Total Operations : {total}\n\n"

        f"Encryptions : {encrypt_count}\n"

        f"Decryptions : {decrypt_count}\n\n"

        f"Characters Processed : {total_characters}\n\n"

        f"Average Shift : {average_shift:.2f}\n"

        f"Most Used Shift : {most_used_shift}"
    )  

def show_chart():

    if not history:
        messagebox.showinfo(
            "Chart",
            "No history available."
        )
        return

    encrypt_count = 0
    decrypt_count = 0

    for item in history:

        if item["Operation"] == "Encrypt":
            encrypt_count += 1
        else:
            decrypt_count += 1

    chart_window = tk.Toplevel(root)
    chart_window.title("Encryption Statistics")
    chart_window.geometry("650x500")

    figure = plt.Figure(figsize=(6, 4), dpi=100)

    ax = figure.add_subplot(111)

    operations = ["Encrypt", "Decrypt"]
    values = [encrypt_count, decrypt_count]

    bars = ax.bar(
    operations,
    values,
    color=["#4CAF50", "#FF9800"]
)

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    ax.set_title(
        "Caesar Cipher Usage Statistics",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Operation",
        fontsize=11
    )

    ax.set_ylabel(
        "Count",
        fontsize=11
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    canvas = FigureCanvasTkAgg(
        figure,
        master=chart_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

def show_pie_chart():

    if not history:
        messagebox.showinfo(
            "Chart",
            "No history available."
        )
        return

    encrypt_count = 0
    decrypt_count = 0

    for item in history:

        if item["Operation"] == "Encrypt":
            encrypt_count += 1
        else:
            decrypt_count += 1

    chart_window = tk.Toplevel(root)
    chart_window.title("Pie Chart")
    chart_window.geometry("600x500")

    figure = plt.Figure(figsize=(6,5), dpi=100)

    ax = figure.add_subplot(111)

    ax.pie(
        [encrypt_count, decrypt_count],
        labels=["Encrypt", "Decrypt"],
        autopct="%1.1f%%",
        colors=["#4CAF50", "#FF9800"],
        startangle=90
    )

    ax.set_title(
        "Caesar Cipher Usage",
        fontsize=14,
        fontweight="bold"
    )

    canvas = FigureCanvasTkAgg(
        figure,
        master=chart_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

def crack_cipher():

    message = input_text.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror(
            "Error",
            "Please enter a cipher text."
        )
        return

    crack_window = tk.Toplevel(root)
    crack_window.title("Caesar Cipher Cracker")
    crack_window.geometry("700x550")

    result_box = tk.Text(
        crack_window,
        wrap="word",
        font=("Consolas", 10)
    )

    result_box.pack(fill="both", expand=True)

    for shift in range(26):

        possible = decrypt(message, shift)

        result_box.insert(
            tk.END,
            f"Shift {shift:2d} : {possible}\n"
        )

    result_box.config(state="disabled")

def update_activity(event=None):
    global last_activity
    last_activity = time.time()


def check_session_timeout():

    if time.time() - last_activity > SESSION_TIMEOUT:

        messagebox.showinfo(
            "Session Expired",
            "Session expired due to inactivity."
        )

        root.destroy()
        return

    root.after(1000, check_session_timeout)

# ---------------- Logged-in User ----------------

if len(sys.argv) > 1:
    logged_in_username = sys.argv[1]
else:
    logged_in_username = "User"

# ---------------- Main Window ----------------

root = tk.Tk()

last_activity = time.time()
SESSION_TIMEOUT = 300   # 5 minutes

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

edit_menu.add_separator()

edit_menu.add_command(
    label="Change Password",
    command=change_password
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
    label="Search History",
    command=search_history
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

statistics_menu = tk.Menu(menu_bar, tearoff=0)

statistics_menu.add_command(
    label="View Statistics",
    command=show_statistics
)

statistics_menu.add_command(
    label="Bar Chart",
    command=show_chart
)

statistics_menu.add_command(
    label="Pie Chart",
    command=show_pie_chart
)


menu_bar.add_cascade(
    label="Statistics",
    menu=statistics_menu
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

welcome_label = tk.Label(
    root,
    text=f"Welcome, {logged_in_username}",
    font=("Segoe UI", 10, "bold"),
    fg="#1565C0",
    bg="#EAF4FC"
)

welcome_label.pack(pady=(0, 5))

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

# ---------------- Cipher ----------------

cipher_frame = tk.Frame(root, bg="#EAF4FC")
cipher_frame.pack(pady=5)

tk.Label(
    cipher_frame,
    text="Cipher",
    font=("Segoe UI", 10, "bold"),
    fg="#0D47A1",
    bg="#EAF4FC"
).pack(side="left", padx=5)

cipher_var = tk.StringVar(value="Caesar")
cipher_var.trace_add("write", update_cipher)

cipher_menu = tk.OptionMenu(
    cipher_frame,
    cipher_var,
    "Caesar",
    "Vigenère",
    "ROT13",
    "Atbash",
    "Rail Fence"
)

cipher_menu.config(
    font=("Segoe UI", 10),
    width=12
)

cipher_menu.pack(side="left")


# ---------------- Shift ----------------

key_label = tk.Label(
    root,
    text="Shift Value",
    font=("Segoe UI", 10, "bold"),
    fg="#0D47A1",
    bg="#EAF4FC"
)
key_label.pack(pady=5)

key_entry = tk.Entry(
    root,
    font=("Segoe UI", 10)
)
key_entry.pack()

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


crack_button = tk.Button(
    button_frame,
    text="🔍 Crack Cipher",
    command=brute_force,
    **button_style
)

crack_button.grid(row=3,column=0,padx=5,pady=5)


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
    crack_button,
    "Try every possible Caesar shift"
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
    exit_button,
    "Close the application"
)

root.protocol("WM_DELETE_WINDOW", exit_program)

# Reset timer on keyboard and mouse activity
root.bind_all("<Key>", update_activity)
root.bind_all("<Button>", update_activity)
root.bind_all("<Motion>", update_activity)

# Start session timeout checker
check_session_timeout()


load_history()

root.mainloop()