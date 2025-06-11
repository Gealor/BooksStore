from typing import TYPE_CHECKING, Optional
from sqlalchemy import CheckConstraint
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
    description : Mapped[str] = mapped_column(default="...", server_default="...", nullable=True)

    borrowed_books : Mapped[list['BorrowedBook']] = relationship(back_populates="book", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            'publication_year > 0 AND publication_year < EXTRACT(YEAR FROM CURRENT_DATE)+1',
            name = 'check_publication_year_range',
        ),
        CheckConstraint(
            'number_copies >= 0',
            name = 'check_number_copies',
        )
    )


