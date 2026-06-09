from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from myapp.application.dto.item import ItemInfoDTO
from myapp.application.interactor.cart import (
    AddItemToCartInteractor,
    RemoveItemFromCartInteractor,
)
from myapp.controllers.schemas.item import RequestItemInfo

router = APIRouter(prefix="/cart", tags=["Корзина"], route_class=DishkaRoute)


@router.post("/item", summary="Добавить товар в корзину")
async def handle_add_item(
    item_request: RequestItemInfo,
    cart_add_item: FromDishka[AddItemToCartInteractor],
):
    item_dto = ItemInfoDTO(
        item_id=item_request.item_id,
        cost=item_request.cost,
        quantity=item_request.quantity,
    )
    await cart_add_item.proceed(item_dto, cart_id=item_request.cart_id)


@router.delete("/item", summary="Удалить товар из корзины")
async def handle_remove_item(
    item_request: RequestItemInfo,
    cart_remove_item: FromDishka[RemoveItemFromCartInteractor],
):
    item_dto = ItemInfoDTO(
        item_id=item_request.item_id,
        cost=item_request.cost,
        quantity=item_request.quantity,
    )
    await cart_remove_item.proceed(item_dto, cart_id=item_request.cart_id)
