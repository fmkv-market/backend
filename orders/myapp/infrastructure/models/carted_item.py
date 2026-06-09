from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from myapp.infrastructure.database import Base


class CartedItemModel(Base):
    __tablename__ = "carted_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column()
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    amount: Mapped[int] = mapped_column()

    __table_args__ = (
        UniqueConstraint("item_id", "cart_id"),
    )