from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from myapp.infrastructure.database import Base


class OrderHistoryModel(Base):
    __tablename__ = "order_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), index=True)
    order_id: Mapped[int] = mapped_column(Integer, unique=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(50))
    items: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    profile: Mapped["ProfileModel"] = relationship("ProfileModel", back_populates="order_history")