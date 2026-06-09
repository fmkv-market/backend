from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from myapp.application.entity.cart import Cart
from myapp.infrastructure.database import Base


class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped = mapped_column(Integer)
    total_price: Mapped = mapped_column(Float)
    total_amount: Mapped = mapped_column(Integer)
    max_quantity: Mapped = mapped_column(Integer, default=20)


    def map_to_domain(self):
        return Cart(
            id=self.id,
            user_id=self.user_id,
            total=self.total_price,
            quantity=self.total_amount
        )


