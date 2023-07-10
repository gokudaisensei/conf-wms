from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared Properties
class InstitutionBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    contactno: Optional[int] = None


# Properties to recieve via API on creation
class InstitutionCreate(InstitutionBase):
    name: str
    address: str
    email: EmailStr
    contactno: int


# Properties to update via API on creation
class InstitutionUpdate(InstitutionBase):
    pass


class InstitutionInDBBase(InstitutionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Properties to return via API
class Institution(InstitutionInDBBase):
    pass


# Properties stored in DB
class InstitutionInDB(InstitutionInDBBase):
    pass
