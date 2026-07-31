def encrypt(text, shift):
    """
    Encrypts the given text using the Caesar Cipher algorithm.

    parameters:
        message (str): The original text to encrypt.
        shift (int): Number of positions to shift each letter.

    returns:
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

    parameters:
        message (str): The encrypted text.
        shift (int): Number of positions used during encryption.

    returns:
        str: The original decrypted message.
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
    
