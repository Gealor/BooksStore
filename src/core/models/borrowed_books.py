from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class BorrowedBook(IntIdPkMixin, Base):
    __tablename__ = 'borrowed_books'

    book_id : Mapped[int] = mapped_column(nullable = False)
    reader_id : Mapped[int] = mapped_column(nullable = False)
    return_date : Mapped[Optional[datetime]] = mapped_column(nullable=True)
    borrow_date : Mapped[datetime] = mapped_column(default = datetime.now(), server_default="now()", nullable = False)

    