from src.cipher import encrypt, decrypt

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
        print("\n✅ Encrypted Message:", encrypted_text)

    elif choice == "2":
        message = input("Enter encrypted message: ")

        try:
            shift = int(input("Enter shift value: "))
        except ValueError:
            print("❌ Invalid shift value! Please enter a number.")
            continue

        decrypted_text = decrypt(message, shift)
        print("\n✅ Decrypted Message:", decrypted_text)

    elif choice == "3":
        print("\n👋 Thank you for using Caesar Cipher Tool!")
        print("Goodbye!")
        break

    else:
        print("\n❌ Invalid choice! Please select 1, 2, or 3.")