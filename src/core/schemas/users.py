from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from core.config import settings


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(min_length=settings.validation.min_len_name)
    email: EmailStr


class UserRead(UserBase):
    id: int
    deleted_at: datetime | None = None


class UserCreate(UserBase):
    password: str = Field(
        min_length=settings.validation.min_len_password,
        max_length=settings.validation.max_len_password,
    )


class UserLoginInfo(UserRead):
    password: str


class UserUpdate(UserCreate):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(
        default=None,
        min_length=settings.validation.min_len_password,
        max_length=settings.validation.max_len_password,
    )


class UserDelete(BaseModel):
    deleted_at: datetime
