import uuid

from sqlalchemy import func, UUID, CheckConstraint, and_, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import CITEXT

from myapp.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    phone: Mapped[str] = mapped_column(
        String,
    )

    first_name: Mapped[str] = mapped_column(
        String,
    )

    second_name: Mapped[str] = mapped_column(
        String,
    )

