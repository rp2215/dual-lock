import os
import json
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

"""
File for dealing with low level cryptographic functions
"""

"""
Function derives cryptographic key from password using supplied salt 
Returns 32-bit cryptographic key
"""
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
            salt=salt, # 256 bit key required for AES-256
            length=32,
            n=2**14,
            r=8,
            p=1,
    )
    return kdf.derive(password.encode())


"""
Function decrypts encrypted master key using `kek`, `nonce`
"""
def decrypt_master_key(kek: bytes, encrypted_master_key: bytes, nonce: bytes) -> bytes:
    return AESGCM(kek).decrypt(
            nonce,
            encrypted_master_key,
            None,
    )

"""
Encrypt values for entry
Return nonce used for entry encryption, and ciphertext
"""
def encrypt_entry(master_key: bytes, site: str, username: str, password: str, notes: str = ""):
    plaintxt = json.dumps({
        "site": site,
        "username": username,
        "password": password,
        "notes": notes
    )}.encode('utf-8')

    nonce = os.urandom(12)
    ciphertxt = AESGCM(master_key).encrypt(
            nonce,
            plaintxt,
            None,
    )

    return nonce, ciphertxt

"""
Decrypt given ciphertext entry given nonce and plaintext masterkey
Returns JSON string of plaintext entry
"""
def decrypt_entry(master_key: bytes, nonce: bytes, ciphertext: bytes):
    data = AESGCM(master_key).decrypt(
            nonce,
            ciphertext,
            None,
    )
    return json.loads(data.decode('utf-8'))
