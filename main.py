from src.cipher import encrypt, decrypt, show_steps, show_decrypt_steps


def save_to_file(operation, original, result, shift):
    """Save encryption/decryption history"""

    with open("history.txt", "a") as file:
        file.write("=" * 40 + "\n")
        file.write(f"Operation : {operation}\n")
        file.write(f"Original  : {original}\n")
        file.write(f"Shift     : {shift}\n")
        file.write(f"Result    : {result}\n")
        file.write("=" * 40 + "\n\n")


def read_from_file(filename):
    """Read text from a file"""

    with open(filename, "r") as file:
        return file.read()


def save_encrypted_file(text):
    """Create/update encrypted_message.txt automatically"""

    with open("encrypted_message.txt", "w") as file:
        file.write(text)


while True:

    print("\n" + "=" * 40)
    print("      CAESAR CIPHER TOOL")
    print("=" * 40)
    print("1. Encrypt Message")
    print("2. Decrypt Message")
    print("3. Encrypt Message From File")
    print("4. Decrypt Message From File")
    print("5. Show Encryption Steps")
    print("6. Show Decryption Steps")
    print("7. Exit")
    print("=" * 40)

    choice = input("Enter your choice (1-7): ")

    # ---------------- Encrypt Message ----------------

    if choice == "1":

        message = input("Enter message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value!")
            continue

        encrypted = encrypt(message, shift)

        save_to_file("Encrypt", message, encrypted, shift)

        print("\n✅ Encrypted Message:")
        print(encrypted)

    # ---------------- Decrypt Message ----------------

    elif choice == "2":

        message = input("Enter encrypted message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value!")
            continue

        decrypted = decrypt(message, shift)

        save_to_file("Decrypt", message, decrypted, shift)

        print("\n✅ Decrypted Message:")
        print(decrypted)

    # ---------------- Encrypt From File ----------------

    elif choice == "3":

        try:
            message = read_from_file("sample_message.txt")

            print("\n📄 Reading sample_message.txt...\n")
            print(message)

            shift = int(input("\nEnter shift value: "))

            encrypted = encrypt(message, shift)

            save_encrypted_file(encrypted)

            save_to_file(
                "Encrypt From File",
                message,
                encrypted,
                shift
            )

            print("\n✅ Encrypted Message:")
            print(encrypted)

            print("\n📁 encrypted_message.txt created successfully!")

        except FileNotFoundError:
            print("❌ sample_message.txt not found.")

        except ValueError:
            print("❌ Invalid shift value!")

    # ---------------- Decrypt From File ----------------

    elif choice == "4":

        try:
            message = read_from_file("encrypted_message.txt")

            print("\n📄 Reading encrypted_message.txt...\n")
            print(message)

            shift = int(input("\nEnter shift value: "))

            decrypted = decrypt(message, shift)

            save_to_file(
                "Decrypt From File",
                message,
                decrypted,
                shift
            )

            print("\n✅ Decrypted Message:")
            print(decrypted)

        except FileNotFoundError:
            print("❌ encrypted_message.txt not found.")
            print("💡 First use Option 3 to create it.")

        except ValueError:
            print("❌ Invalid shift value!")

    # ---------------- Show Encryption Steps ----------------

    elif choice == "5":

        message = input("Enter message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value!")
            continue

        show_steps(message, shift)

    # ---------------- Show Decryption Steps ----------------

    elif choice == "6":

        message = input("Enter encrypted message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value!")
            continue

        show_decrypt_steps(message, shift)

    # ---------------- Exit ----------------

    elif choice == "7":

        print("\n👋 Thank you for using Caesar Cipher Tool!")
        print("Goodbye!")
        break

    else:
        print("\n❌ Invalid choice! Please choose 1-7.")