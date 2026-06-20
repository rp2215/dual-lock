import os
import json
import uuid
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy.orm import Session
from app.database import engine
from app.models.user import User
from app.models.vault import Vault
from app.models.entry import Entry
from app.models.enums import VaultType

# take password and turn into 32-byte crypto key using salt
def derive_key(password, salt):

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def create_vault(password):

    master_key = os.urandom(32) # what actually encrypts entries

    salt = os.urandom(16)
    nonce = os.urandom(12)

    kek = derive_key(password, salt) # gets Key Encryption Key(KEK)

    encrypted_master_key = AESGCM(kek).encrypt(nonce, master_key, None) # encyrpt master key with KEK

    return master_key, salt, nonce, encrypted_master_key


# encyrpts single entry
def encrypt_entry(master_key, site, username, password, notes=""):

    # bundle into a JSON string then convert to bytes
    entry_data = json.dumps({
        "site": site,
        "username": username,
        "password": password,
        "notes": notes
    }).encode("utf-8")

    nonce = os.urandom(12)

    ciphertext = AESGCM(master_key).encrypt(nonce, entry_data, None) # encrypt JSON bytes using vaults master key

    return nonce, ciphertext


def seed():

    ph = PasswordHasher()

    with Session(engine) as db:

        # create test user
        user = User(

            id=uuid.uuid4(),
            email="test@example.com",
            user_password_hash=ph.hash("accountpassword123"),
        )
        db.add(user)
        db.flush() 

        # create real vault
        real_master_key, real_salt, real_nonce, real_encrypted_mk = create_vault("realvaultpassword")
        real_vault = Vault(

            id=uuid.uuid4(),
            user_id=user.id,
            vault_type=VaultType.REAL,
            salt=real_salt,
            master_key_nonce=real_nonce,
            encrypted_master_key=real_encrypted_mk,
        )
        db.add(real_vault)
        db.flush()

        # create duress vault
        duress_master_key, duress_salt, duress_nonce, duress_encrypted_mk = create_vault("duressvaultpassword")
        duress_vault = Vault(

            id=uuid.uuid4(),
            user_id=user.id,
            vault_type=VaultType.DURESS,
            salt=duress_salt,
            master_key_nonce=duress_nonce,
            encrypted_master_key=duress_encrypted_mk,
        )
        db.add(duress_vault)
        db.flush()

        # add real vault entries
        for site, username, password in [
            ("github.com", "testuser@gmail.com", "github_pass392"),
            ("google.com", "testuser@gmail.com", "google_pass456"),
            ("amazon.com", "testuser@gmail.com", "amazon_pass789"),
        ]:
            nonce, ciphertext = encrypt_entry(real_master_key, site, username, password)
            db.add(Entry(id=uuid.uuid4(), vault_id=real_vault.id, nonce=nonce, ciphertext=ciphertext))

        # add duress vault entries 
        for site, username, password in [
            ("facebook.com", "fakeuser@gmail.com", "fake_pass111"),
            ("twitter.com", "fakeuser@gmail.com", "fake_pass222"),
        ]:
            nonce, ciphertext = encrypt_entry(duress_master_key, site, username, password)
            db.add(Entry(id=uuid.uuid4(), vault_id=duress_vault.id, nonce=nonce, ciphertext=ciphertext))

        # save everything in one go if anything fails nothing gets saved
        db.commit()
        print("Seed data inserted successfully")


if __name__ == "__main__":
    seed()
