from datetime import date, datetime

from sqlalchemy import Integer, String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from myapp.infrastructure.database import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    addresses: Mapped[list["AddressModel"]] = relationship(
        "AddressModel", back_populates="profile", cascade="all, delete-orphan"
    )
    order_history: Mapped[list["OrderHistoryModel"]] = relationship(
        "OrderHistoryModel", back_populates="profile", cascade="all, delete-orphan"
    )
