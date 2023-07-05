from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum


# Enumeration of membership
class MembershipEnum(str, Enum):
    Choice1 = "Choice1"
    Choice2 = "Choice2"


# Shared Properties
class InstitutionBase(BaseModel):
    institutionName: Optional[str] = None
    institutionAddress: Optional[str] = None
    email: Optional[EmailStr] = None
    contactNum: Optional[int] = None
    membership: Optional[MembershipEnum] = None


# Properties to recieve via API on creation
class InstitutionCreate(InstitutionBase):
    institutionName: str
    institutionAddress: str
    email: EmailStr
    contactNum: int
    membership: MembershipEnum


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
