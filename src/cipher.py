def encrypt(text, shift):
    """
    Encrypts the given text using the Caesar Cipher algorithm.

    Parameters:
        text (str): The original text.
        shift (int): Number of positions to shift each letter.

    Returns:
        str: The encrypted message.
    """

    result = ""

    for char in text:

        if char.isalpha():

            ascii_value = ord(char)

            if char.isupper():
                position = ascii_value - ord('A')
                new_position = (position + shift) % 26
                new_character = chr(new_position + ord('A'))

            else:
                position = ascii_value - ord('a')
                new_position = (position + shift) % 26
                new_character = chr(new_position + ord('a'))

            result += new_character

        else:
            result += char

    return result


def decrypt(text, shift):
    """
    Decrypts the given text using the Caesar Cipher algorithm.

    Parameters:
        text (str): The encrypted text.
        shift (int): Number of positions used during encryption.

    Returns:
        str: The decrypted message.
    """

    result = ""

    for char in text:

        if char.isalpha():

            ascii_value = ord(char)

            if char.isupper():
                position = ascii_value - ord('A')
                new_position = (position - shift) % 26
                new_character = chr(new_position + ord('A'))

            else:
                position = ascii_value - ord('a')
                new_position = (position - shift) % 26
                new_character = chr(new_position + ord('a'))

            result += new_character

        else:
            result += char

    return result


def show_steps(text, shift):
    """
    Display step-by-step Caesar Cipher encryption.
    """

    print("\n" + "=" * 50)
    print("       STEP-BY-STEP ENCRYPTION")
    print("=" * 50)

    result = ""

    for char in text:

        if char.isalpha():

            encrypted_char = encrypt(char, shift)

            print(f"{char}  --->  {encrypted_char}")

            result += encrypted_char

        else:

            print(f"{char}  --->  {char}")

            result += char

    print("=" * 50)
    print("Final Encrypted Message:")
    print(result)
    print("=" * 50)

    return result


def show_decrypt_steps(text, shift):
    """
    Display step-by-step Caesar Cipher decryption.
    """

    print("\n" + "=" * 50)
    print("       STEP-BY-STEP DECRYPTION")
    print("=" * 50)

    result = ""

    for char in text:

        if char.isalpha():

            decrypted_char = decrypt(char, shift)

            print(f"{char}  --->  {decrypted_char}")

            result += decrypted_char

        else:

            print(f"{char}  --->  {char}")

            result += char

    print("=" * 50)
    print("Final Decrypted Message:")
    print(result)
    print("=" * 50)

    return result