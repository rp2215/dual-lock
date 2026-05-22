class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID, primary_key=True)
    vault_id = Column(UUID, ForeignKey("vaults.id"), nullable=False)
    nonce = Column(BYTEA, nullable=False)
    ciphertext = Column(BYTEA, nullable=False) # encrypted json of all data for this entry 
