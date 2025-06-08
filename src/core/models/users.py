from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


if TYPE_CHECKING:
    from .borrowed_books import BorrowedBook

class User(IntIdPkMixin, Base):
    __tablename__ = 'users'

    email : Mapped[str] = mapped_column(unique = True, nullable = False)
    password : Mapped[str] = mapped_column(nullable = False)
    
    borrowed_books : Mapped[list["BorrowedBook"]] = relationship(back_populates="user", cascade = 'all, delete-orphan')