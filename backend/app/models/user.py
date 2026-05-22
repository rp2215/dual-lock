from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    user_password_hash = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vaults = relationship("Vault",back_populates="user")
