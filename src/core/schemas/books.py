from typing import Optional
from pydantic import BaseModel, Field

from core.config import settings


class BookBase(BaseModel):
    title: str = Field(min_length=settings.validation.min_len_title)
    author: str = Field(min_length=settings.validation.min_len_name)
    ISBN: Optional[str] = Field(
        default=None,
        min_length=settings.validation.len_ISBN,
        max_length=settings.validation.len_ISBN,
    )
    publication_year: Optional[int] = Field(default=None, gt=0)
    number_copies: int = Field(default=1, ge=0)
    description: Optional[str] = Field(
        default=None, max_length=settings.validation.max_len_description
    )


class BookRead(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None, min_length=settings.validation.min_len_title
    )
    author: Optional[str] = Field(
        default=None, min_length=settings.validation.min_len_name
    )
    ISBN: Optional[str] = Field(
        default=None,
        min_length=settings.validation.len_ISBN,
        max_length=settings.validation.len_ISBN,
    )
    publication_year: Optional[int] = Field(default=None, gt=0)
    number_copies: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(
        default=None, max_length=settings.validation.max_len_description
    )


class BookDelete(BaseModel):
    deleted: int


class BookInfo(BaseModel):
    title: str
    author: str
    ISBN: Optional[str] = None
    publication_year: Optional[int] = None
    description: Optional[str] = Field(
        default=None, max_length=settings.validation.max_len_description
    )
