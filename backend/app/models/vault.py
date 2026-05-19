from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.sql import func
from app.database import Base

# class mapping to database table
class VaultEntry(Base):

    __tablename__ = "vault_entries" 

    id = Column(Integer, primary_key=True, index=True)
    vault_type = Column(String, nullable=False) # real or duress
    site_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(LargeBinary, nullable=False) # stored as raw encrypted bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
