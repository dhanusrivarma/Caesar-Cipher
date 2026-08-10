import hashlib

password = input("Enter password: ")

hashed = hashlib.sha256(password.encode()).hexdigest()

print("\nSHA-256 Hash:\n")
print(hashed)