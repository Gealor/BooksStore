from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from core.schemas.books import BookInfo


class BorrowedBookBase(BaseModel):
    book_id: int
    reader_id: int
    return_date: Optional[datetime] = None
    borrow_date: Optional[datetime] = None


class BorrowedBookRead(BorrowedBookBase):
    id: int


class BorrowedBookCreate(BorrowedBookBase):
    pass


class BorrowedBookUpdate(BaseModel):
    # если указать просто datetime.now(), то значение по умолчанию поставится в момент определения класса, т.е. при запуске приложения
    # надо указывать фабрику, которая при каждом создании экземпляра будет вызывать дополнительно эту фабрику.
    return_date: datetime = Field(default_factory=datetime.now)


class BorrowedBookDelete(BaseModel):
    deleted: int


class BorrowedBookInfo(BaseModel):
    record_id: int = Field(alias="id")
    book: BookInfo


class BorrowedBookWithDate(BorrowedBookInfo):
    id: int
    return_date: Optional[datetime] = None
    borrow_date: datetime
