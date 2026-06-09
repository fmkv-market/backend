from sqlalchemy.orm import Mapped, mapped_column

from myapp.application.entity.cart import Cart
from myapp.infrastructure.database import Base


class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column()
    total_price: Mapped[float] = mapped_column()
    total_amount: Mapped[int] = mapped_column()
    max_quantity: Mapped[int] = mapped_column(default=20)

    def map_to_domain(self) -> Cart:
        return Cart(
            id=self.id,
            user_id=self.user_id,
            total=self.total_price,
            quantity=self.total_amount,
        )


