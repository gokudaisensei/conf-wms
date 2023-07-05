from enum import Enum
from pydantic import BaseModel, EmailStr
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
    institution: Optional[Institution] = None


# Properties to recieve via API on creation
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    enabled: bool = False


# Properties to update via API on creation
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str