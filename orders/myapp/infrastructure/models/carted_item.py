from sqlalchemy import Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from myapp.infrastructure.database import Base


class CartedItemModel(Base):
    __tablename__ = "carted_item"
    item_id: Mapped = mapped_column(Integer)
    cart_id: Mapped = mapped_column(ForeignKey("cart.id"))
    amount: Mapped = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("item_id", "cart_id"),
    )