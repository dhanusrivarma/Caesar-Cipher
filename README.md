# 🔐 Caesar Cipher Pro

A professional Python implementation of the **Caesar Cipher** encryption algorithm with an interactive command-line interface, file encryption support, learning mode, history logging, and automated testing.

---

## 📖 Project Description

Caesar Cipher Pro is a Python application that demonstrates the Caesar Cipher encryption technique. It is designed not only to encrypt and decrypt messages but also to help beginners understand how the algorithm works through a dedicated **Learning Mode**.

The project follows a modular structure and includes file handling, exception handling, automated testing, and Git version control.

---

## ✨ Features

- 🔒 Encrypt messages
- 🔓 Decrypt messages
- 📂 Encrypt text from a file
- 📂 Decrypt text from a file
- 📄 Automatically generates `encrypted_message.txt`
- 📝 Saves operation history to `history.txt`
- 🎓 Learning Mode with step-by-step encryption
- 🎓 Learning Mode with step-by-step decryption
- ✅ Input validation
- 🔤 Supports uppercase and lowercase letters
- 🔢 Preserves numbers, spaces, and symbols
- 🧪 Automated testing using Pytest
- 📁 Modular project structure

---

## 📂 Project Structure

```text
Caesar-Cipher-Pro/
│
├── src/
│   ├── __init__.py
│   └── cipher.py
│
├── tests/
│   ├── __init__.py
│   └── test_cipher.py
│
├── sample_message.txt
├── history.txt
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project folder:

```bash
cd Caesar-Cipher-Pro
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python login.py
```

---

## 🧪 Running Tests

Run all tests using Pytest:

```bash
python -m pytest
```

Expected output:

```text
9 passed
```

---

## 📚 Learning Mode

The project includes a dedicated learning mode that displays Caesar Cipher operations step by step.

Example:

```
h ---> k
e ---> h
l ---> o
l ---> o
o ---> r
```

This feature helps beginners understand how each character is transformed.

---

## 🛠 Technologies Used

- Python 3
- Pytest
- Git
- GitHub
- VS Code

---

## 🚀 Future Improvements

- Desktop GUI using Tkinter
- Flask Web Application
- Password-protected encryption
- Multiple cipher algorithms
- Save history in JSON format
- Export history as PDF
- Dark mode GUI
---

## 👩‍💻 Author

**Dhanu Sri**

B.Tech CSM Student

Python Developer | AI & Machine Learning Aspirant

---

## 📄 License

This project is developed for educational purposes.