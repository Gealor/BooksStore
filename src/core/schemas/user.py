

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name : str
    email : EmailStr

class UserRead(UserBase):
    id : int

class UserCreate(UserBase):
    password : str

class UserUpdate(UserCreate):
    name : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None

class UserDelete(BaseModel):
    deleted : int
