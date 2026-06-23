import uuid
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.vault_service import create_user_vaults

"""
File for user-related business logic
"""

ph = PasswordHasher()

"""
Function to create user and init vault
Returns User object that has been added
Throws ValueError if user already exists with the same email 
"""
def create_user(db: Session, email: str, password: str) -> User:
    user_exists = get_user_by_email(db,email)
    if user_exists:
        raise ValueError("User already exists")

    password_hash = ph.hash(password)

    user = User(
            id=uuid.uuid4(),
            email=email,
            user_password_hash=password_hash,
    )

    db.add(user)
    db.flush()

    ## TODO: Optionally call `create_user_vault` here

    db.commit()
    db.refresh(user)

    return user


#####-USER-LOOKUP-FUNCTIONS-#####
"""
Retrieve User entry by email
Returns User if exists
"""
def get_user_by_email(db: Session, email: str) -> User | None:
    # Note: multiple users with this email (shouldn't exist) will cause an error to be raised, which needs caught in caller
    return db.scalars(
            select(User).where(User.email == email)
    ).one_or_none()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.scalars(
            select(User).where(User.id == user_id)
    ).one_or_none()


"""
Compares user entered password to stored hash for this user
Returns True if same, False else
"""
def verify_user_password(user: User, password: str) -> bool:
    try:
        return ph.verify(user.user_password_hash,password)
    except Exception:
        # exception may be due to incorrect password, or failure to hash/compare
        return False
