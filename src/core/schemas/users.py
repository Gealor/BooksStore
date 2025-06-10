
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from core.config import settings

class UserBase(BaseModel):
    name : str = Field(min_length=settings.validation.min_len_name)
    email : EmailStr

class UserRead(UserBase):
    id : int

class UserCreate(UserBase):
    password : str = Field(
        min_length=settings.validation.min_len_password, 
        max_length=settings.validation.max_len_password
    )

class UserLoginInfo(UserRead):
    password : str

class UserUpdate(UserCreate):
    name : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = Field(
        default=None, 
        min_length=settings.validation.min_len_password, 
        max_length=settings.validation.max_len_password
    )


class UserDelete(BaseModel):
    deleted : int


