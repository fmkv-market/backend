import uuid

from sqlalchemy import func, UUID, CheckConstraint, and_, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT

from myapp.infrastructure.database import Base
from myapp.infrastructure.models.addresses import AddressModel


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

    is_blocked: Mapped[bool] = mapped_column(default=False)

    address_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("addresses.id"), nullable=True
    )
    address: Mapped[AddressModel | None] = relationship(
        "AddressModel", back_populates="users"
    )
