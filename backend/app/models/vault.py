from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import VaultType


class Vault(Base):
    __tablename__ = "vaults" 

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    vault_type = Column(Enum(VaultType), nullable=False, default=VaultType.REAL)

    salt = Column(BYTEA, nullable=False)
    master_key_nonce = Column(BYTEA, nullable=False)
    encrypted_master_key = Column(BYTEA, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="vaults")
