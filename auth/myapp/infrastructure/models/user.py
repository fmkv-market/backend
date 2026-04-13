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

    email: Mapped[str] = mapped_column(
        CITEXT,
        unique=True,
    )

    phone: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    hash_password: Mapped[str] = mapped_column(String(200))

