from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    __tablename__ = 'users'

    email : Mapped[str] = mapped_column(unique = True, nullable = False)
    password : Mapped[str] = mapped_column(nullable = False)
    