from src.cipher import encrypt, decrypt


def test_encrypt_lowercase():
    assert encrypt("hello", 3) == "khoor"


def test_decrypt_lowercase():
    assert decrypt("khoor", 3) == "hello"


def test_encrypt_uppercase():
    assert encrypt("HELLO", 3) == "KHOOR"


def test_decrypt_uppercase():
    assert decrypt("KHOOR", 3) == "HELLO"


def test_numbers_unchanged():
    assert encrypt("abc123", 3) == "def123"


def test_symbols_unchanged():
    assert encrypt("Hello!", 3) == "Khoor!"


def test_shift_zero():
    assert encrypt("Python", 0) == "Python"


def test_large_shift():
    assert encrypt("abc", 29) == "def"


def test_negative_shift():
    assert encrypt("def", -3) == "abc"