from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.borrowed_books import BorrowedBook
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .borrowed_books import BorrowedBook

class Book(IntIdPkMixin, Base):
    __tablename__ = 'books'

    title : Mapped[str] = mapped_column(nullable = False)
    author : Mapped[str] = mapped_column(nullable = False)
    publication_year : Mapped[Optional[int]] = mapped_column(nullable = True)
    ISBN : Mapped[Optional[str]] = mapped_column(unique = True, nullable = True)
    number_copies : Mapped[int] = mapped_column(default=1, nullable = False)

    borrowed_books : Mapped[list['BorrowedBook']] = relationship(back_populates="book", cascade="all, delete-orphan")


