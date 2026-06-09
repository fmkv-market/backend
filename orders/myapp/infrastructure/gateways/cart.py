from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.cart import CartDTO
from myapp.application.entity.cart import Cart
from myapp.application.interface.cart import CartSaver, CartReader
from myapp.infrastructure.models.cart import CartModel
from myapp.infrastructure.models.carted_item import CartedItemModel


class CartGateway(CartSaver, CartReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, cart: Cart) -> Cart:
        if cart.id is None:
            cart_db = CartModel(user_id=cart.user_id, total_price=cart.total, total_amount=cart.quantity)
            self.session.add(cart_db)
            await self.session.flush()
            cart.id = cart_db.id
        else:
            cart_db = (
                await self.session.execute(select(CartModel).where(CartModel.id == cart.id))
            ).scalars().first()
            cart_db.total_price = cart.total
            cart_db.total_amount = cart.quantity

            for item_id, amount in cart.items.items():
                carted_item = (await self.session.execute(
                    select(CartedItemModel).where(
                        CartedItemModel.cart_id == cart.id,
                        CartedItemModel.item_id == item_id,
                    )
                )).scalars().first()

                if carted_item:
                    carted_item.amount = amount
                else:
                    self.session.add(CartedItemModel(cart_id=cart.id, item_id=item_id, amount=amount))

            await self.session.execute(
                delete(CartedItemModel).where(
                    CartedItemModel.cart_id == cart.id,
                    ~CartedItemModel.item_id.in_(cart.items.keys()),
                )
            )

        await self.session.commit()
        return cart

    async def read_by_id(self, cart_id: int) -> CartDTO | None:
        cart_db = (
            await self.session.execute(select(CartModel).where(CartModel.id == cart_id))
        ).scalars().first()
        if cart_db is None:
            return None
        return CartDTO(id=cart_db.id, user_id=cart_db.user_id, total=cart_db.total_price, quantity=cart_db.total_amount)

    async def read_by_user_id(self, user_id: int) -> CartDTO | None:
        cart_db = (
            await self.session.execute(select(CartModel).where(CartModel.user_id == user_id))
        ).scalars().first()
        if cart_db is None:
            return None
        return CartDTO(id=cart_db.id, user_id=cart_db.user_id, total=cart_db.total_price, quantity=cart_db.total_amount)