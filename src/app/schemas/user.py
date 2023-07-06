from enum import Enum
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional

from app.schemas.institution import Institution


# Enumeration of roles
class RoleEnum(str, Enum):
    SuperAdmin = "SuperAdmin"
    Admin = "Admin"
    Coordinator = "Coordinator"
    Editor = "Editor"
    AssociateEditor = "AssociateEditor"
    Reviewer = "Reviewer"
    Author = "Author"


# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    roleID: Optional[RoleEnum] = None
    enabled: Optional[bool] = False


# Properties to recieve via API on creation
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: SecretStr
    institution_id: Optional[int] = None


# Properties to update via API on creation
class UserUpdate(UserBase):
    password: Optional[SecretStr] = None
    institution_id: Optional[int] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    institution: Optional[Institution] = None

    class Config:
        orm_mode = True


# Properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
