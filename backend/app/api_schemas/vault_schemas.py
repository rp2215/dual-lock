from pydantic import BaseModel
from datetime import datetime

# Defines data shapes that the vault API will use

class VaultEntryCreate(BaseModel):
    site_name: str
    username: str
    password: str
    notes: str | None = None 

# front end only sends whats changed
# all fields optional 
class VaultEntryUpdate(BaseModel):
    site_name: str | None = None
    username: str | None = None
    password: str | None = None
    notes: str | None = None


# shape of data sent back to frontend
class VaultEntryResponse(BaseModel):
    id: int
    site_name: str
    username: str
    password: str # plain decrypted string
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True} # tells Pydantic its allowed to read data directly from model objects
