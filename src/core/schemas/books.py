


from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title : str
    author : str
    ISBN : Optional[str] = None
    publication_year : Optional[int] = None
    number_copies : int = 1

class BookRead(BookBase):
    id : int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    ISBN : Optional[str] = None
    publication_year : Optional[int] = None
    number_copies : Optional[int] = None

class BookDelete(BaseModel):
    deleted : int

class BookInfo(BaseModel):
    title : str
    author : str
    ISBN : Optional[str] = None
    publication_year : Optional[int] = None
