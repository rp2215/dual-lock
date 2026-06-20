import os
import json
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

vault_password = "password123"
fake_vault_password = "cars"

# generate cryptographically random 32-bit master key
master_key=os.urandom(32)

# generate random salt to be used later
# 128 bits of salt
random_salt=os.urandom(16)


# derive key encryption key
# vault password becomes a cryptographic key
# human password --> complex cryptographic key
def derive_key(password,salt):
    kdf=Scrypt(
            salt=salt,
            length=32, # 256 bit key required for AES-256
            n=2**14, # make CPU cost high
            r=8, # memory usage
            p=1, # paralleization cost
    )
    # returns 32-bit cryptographic key
    # encode turns string password into bytes
    return kdf.derive(password.encode())

key_encrypted_key=derive_key(vault_password,random_salt)
#print(key_encrypted_key)


# create AESGCM object of KEK
# any changes to this will cause it to fail decryption
aesgcm= AESGCM(key_encrypted_key)

# create random number associated with the master key
master_key_nonce=os.urandom(12)

# generates unreadable ciphertext
encrypted_master_key=aesgcm.encrypt(
        master_key_nonce,
        master_key, # some random bits 
        None
)
print(encrypted_master_key)



# password that the user enters when attempting to login and view their vault
entered_password="something"

kek=derive_key(entered_password,stored_user["vault_salt"])


##########################################
"""
Decrypt the master key in order to be able to access the entries
"""
# if same password is entered, this should create an identical object - thus allow us to decrypt correctly
aesgcm = AESGCM(kek)

master_key = aesgcm.decrypt(
        stored_user["master_key_nonce"],
        stored_user["encrypted_master_key"],
        None
)
##########################################

##########################################
"""
Decrypt entry
Master key has been decrypted, so use that for the entry
"""
entry_aesgm=AESGCM(master_key)
plaintext = entry_aesgm.decrypt(
        stored_user["none"], # value used for **this** specific entry
        stored_user["ciphertext"], # actual encrypted data
        None
)
entry=json.loads(plaintext.decode()) # assuming stored_user["ciphertext"] is stored in json format
##########################################
