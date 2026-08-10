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


# ---------------- Atbash Cipher ----------------

def atbash(text):
    """
    Encrypts or decrypts text using the Atbash Cipher.

    Atbash replaces:
    A → Z
    B → Y
    C → X
    ...
    Z → A

    The same function is used for both encryption and decryption.
    """

    result = ""

    for char in text:

        if char.isupper():
            result += chr(ord('Z') - (ord(char) - ord('A')))

        elif char.islower():
            result += chr(ord('z') - (ord(char) - ord('a')))

        else:
            result += char

    return result

# ---------------- Rail Fence Cipher ----------------

def rail_fence_encrypt(text, rails):
    """
    Encrypts text using the Rail Fence Cipher.
    """

    if rails <= 1 or rails >= len(text):
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
