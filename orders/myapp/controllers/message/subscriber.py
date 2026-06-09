from dishka import FromDishka
from faststream.rabbit import RabbitRouter, RabbitQueue
from dishka_faststream import inject as faststream_inject

from myapp.application.dto.cart import CreateCartDTO
from myapp.application.dto.item import ItemInfoDTO
from myapp.application.interactor.cart import (
    CreateCartInteractor,
    AddItemToCartInteractor,
    RemoveItemFromCartInteractor,
)
from myapp.controllers.schemas.item import RequestItemInfo
from myapp.infrastructure.message.config import QueueConfig

router = RabbitRouter()


@router.subscriber(RabbitQueue(name=QueueConfig.user_created, durable=True))
@faststream_inject
async def handle_user_created(
        user_id: int,
        cart_creator: FromDishka[CreateCartInteractor],
):
    cart_dto = CreateCartDTO(user_id=user_id)
    await cart_creator.proceed(cart_dto)


@router.subscriber(RabbitQueue(name=QueueConfig.item_added, durable=True))
@faststream_inject
async def handle_item_added(
        item_request: RequestItemInfo,
        cart_add_item: FromDishka[AddItemToCartInteractor],
):
    item_dto = ItemInfoDTO(
        item_id=item_request.item_id,
        cost=item_request.cost,
        quantity=item_request.quantity
    )
    await cart_add_item.proceed(item_dto, cart_id=item_request.cart_id)


@router.subscriber(RabbitQueue(name=QueueConfig.item_removed, durable=True))
@faststream_inject
async def handle_item_removed(
        item_request: RequestItemInfo,
        cart_remove_item: FromDishka[RemoveItemFromCartInteractor],
):
    item_dto = ItemInfoDTO(
        item_id=item_request.item_id,
        cost=item_request.cost,
        quantity=item_request.quantity
    )
    await cart_remove_item.proceed(item_dto, cart_id=item_request.cart_id)
