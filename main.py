from src.cipher import encrypt, decrypt


def save_to_file(operation, original, result, shift):
    """Save encryption/decryption history to history.txt"""

    with open("history.txt", "a") as file:
        file.write("=" * 40 + "\n")
        file.write(f"Operation : {operation}\n")
        file.write(f"Original  : {original}\n")
        file.write(f"Shift     : {shift}\n")
        file.write(f"Result    : {result}\n")
        file.write("=" * 40 + "\n\n")


while True:
    print("\n" + "=" * 40)
    print("      CAESAR CIPHER TOOL")
    print("=" * 40)
    print("1. Encrypt Message")
    print("2. Decrypt Message")
    print("3. Exit")
    print("=" * 40)

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        message = input("Enter message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value! Please enter a number.")
            continue

        encrypted_text = encrypt(message, shift)

        save_to_file("Encrypt", message, encrypted_text, shift)

        print("\n✅ Encrypted Message:", encrypted_text)

    elif choice == "2":
        message = input("Enter encrypted message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value! Please enter a number.")
            continue

        decrypted_text = decrypt(message, shift)

        save_to_file("Decrypt", message, decrypted_text, shift)

        print("\n✅ Decrypted Message:", decrypted_text)

    elif choice == "3":
        print("\n👋 Thank you for using Caesar Cipher Tool!")
        print("Goodbye!")
        break

    else:
        print("\n❌ Invalid choice! Please select 1, 2, or 3.")