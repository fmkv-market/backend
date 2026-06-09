from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.base import BaseDTO
from myapp.application.dto.cart import CartDTO
from myapp.application.entity.cart import Cart
from myapp.application.interface.cart import CartSaver, CartReader, CartUpdater
from myapp.infrastructure.models.cart import CartModel
from myapp.infrastructure.models.carted_item import CartedItemModel


class CartGateway(CartSaver, CartReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, cart: Cart) -> Cart:
        _cart_db = (
            await self.session.execute(
                select(CartModel)
                .where(CartModel.id == cart.id))
        ).scalars().first()

        _cart_db.total = cart.total
        _cart_db.quantity = cart.quantity

        for item_id, amount in cart.items:
            carted_item = (await self.session.execute(
                select(CartedItemModel)
                .where(CartedItemModel.item_id == item_id)
            )).scalars().first()

            carted_item.amount = amount
            carted_item.cart_id = cart.id
        item_ids_to_delete = (await self.session.execute(select(CartedItemModel.item_id).where(
            CartedItemModel.cart_id == cart.id,
            ~CartedItemModel.item_id.in_(cart.items.keys())
        ))).scalars().all()
        stmt = delete(CartedItemModel).where(CartedItemModel.item_id.in_(item_ids_to_delete))
        await self.session.execute(stmt)
        return cart


    async def read_by_id(self, cart_id: int) -> CartDTO: ...
    async def read_by_user_id(self, user_id: int) -> CartDTO: ...

