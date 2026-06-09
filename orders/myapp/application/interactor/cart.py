from myapp.application.dto.cart import CreateCartDTO
from myapp.application.dto.item import ItemInfoDTO
from myapp.application.entity.cart import Cart

from myapp.application.interface.cart import (
    CartReader,
    CartSaver,
)


class CreateCartInteractor:
    def __init__(self, saver: CartSaver):
        self.saver = saver

    async def proceed(self, cart_info: CreateCartDTO) -> Cart:
        cart = Cart(user_id=cart_info.user_id, total=0, quantity=0)
        await self.saver.save(cart)
        return cart


class AddItemToCartInteractor:
    def __init__(self, saver: CartSaver, reader: CartReader):
        self.saver = saver
        self.reader = reader

    async def proceed(self, item: ItemInfoDTO, cart_id: int) -> None:
        cart_dto = await self.reader.read_by_id(cart_id)
        if cart_dto is None:
            return
        cart = Cart(
            id=cart_dto.id,
            user_id=cart_dto.user_id,
            total=cart_dto.total,
            quantity=cart_dto.quantity,
        )
        cart.add_item(item.item_id, item.quantity, item.cost)
        await self.saver.save(cart)


class RemoveItemFromCartInteractor:
    def __init__(self, saver: CartSaver, reader: CartReader):
        self.saver = saver
        self.reader = reader

    async def proceed(self, item: ItemInfoDTO, cart_id: int) -> None:
        cart_dto = await self.reader.read_by_id(cart_id)
        if cart_dto is None:
            return
        cart = Cart(
            id=cart_dto.id,
            user_id=cart_dto.user_id,
            total=cart_dto.total,
            quantity=cart_dto.quantity,
        )
        cart.remove_item(item.item_id, item.cost, item.quantity)
        await self.saver.save(cart)