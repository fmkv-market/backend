from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response

from myapp.application.dto.address import AddressCreate
from myapp.application.exception.address import AddressNotFoundException
from myapp.application.exception.profile import ProfileNotFoundException
from myapp.application.interactor.address import (
    AddAddressInteractor,
    DeleteAddressInteractor,
    GetAddressesInteractor,
    SetDefaultAddressInteractor,
)
from myapp.controllers.exceptions import AddressNotFoundHTTPException, ProfileNotFoundHTTPException
from myapp.controllers.schemas.address import AddressCreateRequest, AddressResponse

router = APIRouter(prefix="/profile", tags=["Адреса"], route_class=DishkaRoute)


@router.get("/{user_id}/addresses", summary="Получить адреса пользователя")
async def get_addresses(
    user_id: int,
    interactor: FromDishka[GetAddressesInteractor],
) -> list[AddressResponse]:
    try:
        addresses = await interactor.execute(user_id)
    except ProfileNotFoundException:
        raise ProfileNotFoundHTTPException
    return [AddressResponse.model_validate(a.model_dump()) for a in addresses]


@router.post("/{user_id}/addresses", summary="Добавить адрес")
async def add_address(
    user_id: int,
    data: AddressCreateRequest,
    interactor: FromDishka[AddAddressInteractor],
) -> AddressResponse:
    try:
        address_dto = AddressCreate(profile_id=0, **data.model_dump(exclude_none=True))
        address = await interactor.execute(user_id, address_dto)
    except ProfileNotFoundException:
        raise ProfileNotFoundHTTPException
    return AddressResponse.model_validate(address.model_dump())


@router.delete("/{user_id}/addresses/{address_id}", summary="Удалить адрес")
async def delete_address(
    user_id: int,
    address_id: int,
    interactor: FromDishka[DeleteAddressInteractor],
) -> Response:
    try:
        await interactor.execute(address_id)
    except AddressNotFoundException:
        raise AddressNotFoundHTTPException
    return Response(status_code=204)


@router.put("/{user_id}/addresses/{address_id}/default", summary="Сделать адрес основным")
async def set_default_address(
    user_id: int,
    address_id: int,
    interactor: FromDishka[SetDefaultAddressInteractor],
) -> Response:
    try:
        await interactor.execute(user_id, address_id)
    except (ProfileNotFoundException, AddressNotFoundException):
        raise AddressNotFoundHTTPException
    return Response(status_code=200)
