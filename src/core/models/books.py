import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Book(IntIdPkMixin, Base):
    __tablename__ = 'books'

    title : Mapped[str] = mapped_column(nullable = False)
    author : Mapped[str] = mapped_column(nullable = False)
    publication_year : Mapped[int] = mapped_column(nullable = True)
    ISBN : Mapped[str] = mapped_column(unique = True, nullable = True)
    number_copies : Mapped[int] = mapped_column(default=1, nullable = False)


