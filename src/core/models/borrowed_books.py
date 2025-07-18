from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin
from core.models.users import User

if TYPE_CHECKING:
    from .users import User
    from .books import Book


class BorrowedBook(IntIdPkMixin, Base):
    __tablename__ = "borrowed_books"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    return_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    # передаю саму функцию now, а не результат ее вызова now(), т.к. значение по умолчанию определяется в момент определения класса
    borrow_date: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default="now()", nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="borrowed_books")
    book: Mapped["Book"] = relationship(back_populates="borrowed_books")
