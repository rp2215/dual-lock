from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.sql import func
from app.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID, primary_key=True)
    vault_id = Column(UUID, ForeignKey("vaults.id"), nullable=False)
    nonce = Column(BYTEA, nullable=False)
    ciphertext = Column(BYTEA, nullable=False) # encrypted json of all data for this entry
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
