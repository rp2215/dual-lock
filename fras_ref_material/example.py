from cryptography.fernet import Fernet
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os 
import json 
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


## INIT ACCOUNT:
def hash_password(plaintext_password):
    ph = PasswordHasher()
    p_hashed = ph.hash(plaintext_password) # salt contained within this password
    return p_hashed

# email and plaintext_password passed from react front 
pasword_hash=hash_password(plaintext_password)

# call function to create user account and pass it the hash_password (and email)


### CREATE VAULT N
## Recieve vault type, vault master password (plaintext)

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

## call db function for adding data
create_new_vault(vault_type,salt,master_key_nonce,encrypted_master_key)
# created/updated calced in function - vault type enum



### CREATE NEW ENTRY IN EXISTING VAULT:
# Recieve entry username, pass, site, and notes

entry = ["username", "password", "site", "notes"]
plaintext_json_data=json.dumps(entry).encode('utf-8') # turn into json 

entry_nonce=os.urandom(12)

## encrypt json using the vault password
# presume vault pass is in mem at this point (since vault needs to be open for adding) ???
aesgcm = AESGCM(decrypted_vault_password)
ciphertext = aesgcm.encrypt(
        entry_nonce,
        plaintext_json_data,
        None,
)

## call function to add entry to db
add_entry(entry_nonce,ciphertext) # rest of fields added in func or auto by db


### DECRYPTING VAULT:
## receive the password that the user has entered for their vault pass

kek=derive_key(user_given_pass,db_vault_salt)
aesgm = AESGCM(kek)
master_key_nonce = 123 # will have retrieved this at an earlier point alonside the other information req for vault

## may fail depending on if password is correct
plaintext_master_key = aesgcm.decrypt(
        master_key_nonce,
        master_key_from_db,
        None,
)

# plaintext_master_key can then be used at later times for decryption of entries

## ENTRY DECRYPTING:
# name of the entry given by user for sourcing 
details = get_entry(name) # array
kek=derive_key(user_given_pass,db_vault_salt) # user given pass may be stored in mem at this point?
aesgcm=AESGCM(kek)
plaintext=aesgcm.decrypt(
        details["nonce"],
        details["ciphertext"],
        None,
)

entry=json.loads(plaintext.decode("utf-8")) # string/array
