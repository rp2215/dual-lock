from cryptography.fernet import Fernet
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os 
import json 
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


## HASHING OF USER PASS
ph = PasswordHasher()
user_pass="secret_password"
p_hashed = ph.hash(user_pass) # salt contained within this password
print(f"Hashed pass: {p_hashed}")
incorrect_pass = "secret password"

try:
    ph.verify(p_hashed,incorrect_pass)
    print("Passwords match")
except VerifyMismatchError:
    print("Passwords do not match")
except InvalidHashError:
    print("An error occured comparing passwords")

del user_pass
print(user_pass)
