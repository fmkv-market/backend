
from sqlalchemy import Integer, String, Float, CheckConstraint, and_, column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from myapp.infrastructure.database import Base


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    small_img: Mapped[str] = mapped_column(String, nullable=True)
    big_img: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String(1000))
    weight: Mapped[float] = mapped_column(Float)
    cost: Mapped[float] = mapped_column(Float)
    composition: Mapped[str] = mapped_column(String)
    expiration_days: Mapped[int] = mapped_column(Integer, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            and_(
                column("weight") >= 0,
                column("cost") >= 0
            )
        ),
    )
