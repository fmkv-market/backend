from myapp.application.dto.cart import CreateCartDTO
from myapp.application.dto.item import ItemInfoDTO
from myapp.application.entity.cart import Cart

from myapp.application.interface.cart import (
    CartReader,
    CartUpdater,
    CartSaver,
)


class CreateCartInteractor:
    def __init__(self, saver: CartSaver):
        self.saver = saver

    async def proceed(self, cart_info: CreateCartDTO) -> Cart:
        cart = Cart(user_id=cart_info.user_id, total=0, quantity=0)
        _cart_from_db = await self.saver.save(cart)
        cart.id = _cart_from_db.id
        return cart


class AddItemToCartInteractor:
    def __init__(self, saver: CartSaver, reader: CartReader):
        self.saver = saver
        self.reader = reader

    async def proceed(self, item: ItemInfoDTO, cart_id: int):
        _cart_from_db = await self.reader.read_by_id(cart_id)
        if _cart_from_db:
            cart = Cart(
                id=_cart_from_db.id,
                user_id=_cart_from_db.user_id,
                total=_cart_from_db.total,
                quantity=_cart_from_db.quantity
            )
            cart.add_item(item.item_id, item.quantity, item.cost)
            cart = await self.saver.save(cart)
            cartDTO = CartDTO


class RemoveItemFromCartInteractor:
    def __init__(self, updater: CartUpdater, reader: CartReader):
        self.updater = updater
        self.reader = reader

    async def proceed(self, item: ItemInfoDTO, cart_id: int):
        _cart_from_db = self.reader.read_by_id(cart_id)
        if _cart_from_db:
            cart = Cart(
                id=_cart_from_db.id,
                user_id=_cart_from_db.user_id,
                total=_cart_from_db.total,
                quantity=_cart_from_db.quantity
            )
            cart.remove_item(item.item_id, item.cost, item.quantity)
            self.updater.remove_item(cart_id, item)
