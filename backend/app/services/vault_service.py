import os
import uuid
import sys
from sqlalchemy.orm import Session
from app.models.vault import Vault
from app.models.entry import Entry
from app.models.enums import VaultType

from app.services.crypto_service import (
    derive_kek,
    encrypt_master_key,
    decrypt_master_key,
    encrypt_entry,
    decrypt_entry
)


"""
Create user vault of specified type
"""
def create_user_vault(db: Session, user_id: str, master_password: str, vault_type: VaultType):
    master_key = os.urandom(32)
    salt = os.urandom(16)
    nonce = os.urandom(12)

    kek = derive_key(master_password,salt)

    encrypt_master_key = encrypt_master_key(kek,master_key,nonce)

    vault = Vault(
            id=uuid.uuid4(),
            user_id=user_id,
            vault_type=vault_type,
            salt=salt,
            master_key_nonce=nonce,
            encrypt_master_key=encrypt_master_key,
    )

    db.add(vault)
    db.flush()

    return vault


"""
Create real vault for user
"""
def create_real_vault(db: Session, user_id: str, master_password: str):
    return real_vault = create_vault(db,user_id,master_password,VaultType.REAL)

"""
Create duress vault for user
"""
def create_duress_vault(db: Session, user_id: str, master_password: str):
    return duress_vault = create_vault(db,user_id,master_password,VaultType.DURESS)


"""
Unlock user vault
Return master_key for later use
"""
def unlock_vault(vault: Vault, master_password: str) -> bytes:
    kek = derive_key(master_password,vault.salt)

    master_key = decrypt_master_key(
            kek,
            vault.encrypt_master_key,
            vault.master_key_nonce,
    )

    return master_key

"""
Create new encrypted entry and add to user's vault
"""
def add_entry(db: Session, vault: Vault, master_key: bytes, site: str, username: str, password: str, notes: str=""):
    nonce, ciphertxt = encrypt_entry(master_key,site,username,password,notes)

    entry = Entry(
            id=uuid.uuid4(),
            vault_id=vault_id,
            nonce=nonce,
            ciphertext=ciphertext
    )

    db.add(entry)
    db.commit()

    return entry

def get_decrypted_entries(db: Session, vault: Vault, master_key: bytes):
    entries = db.scalars(
            select(Entry).where(Entry.vault_id == vault.id)
    ).all()

    results = []

    for entry in entries:
        decrypted = decrypt_entry(master_key,entry.nonce,entry.ciphertext)
        results.append(decrypted)

    return results
