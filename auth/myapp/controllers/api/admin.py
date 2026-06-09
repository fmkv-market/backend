from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response

from myapp.application.interactor.block_user import BlockUserInteractor
from myapp.application.interactor.change_password import AdminChangePasswordInteractor
from myapp.infrastructure.exceptions.user import UserNotFoundException

from myapp.controllers.exceptions import UserNotFoundHTTPException
from myapp.controllers.schemas.email import AdminPasswordReset

router = APIRouter(prefix="/admin", tags=["Безопасность"], route_class=DishkaRoute)


@router.post(
    "/users/{user_id}/reset-password",
    summary="Принудительная смена пароля пользователя администратором",
)
async def reset_user_password(
        user_id: int,
        data: AdminPasswordReset,
        change_password_executor: FromDishka[AdminChangePasswordInteractor],
) -> Response:
    try:
        await change_password_executor.execute(user_id=user_id, new_password=data.new_password)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return Response(status_code=200)


@router.post(
    "/users/{user_id}/block",
    summary="Заблокировать учётную запись пользователя",
)
async def block_user(
        user_id: int,
        executor: FromDishka[BlockUserInteractor],
) -> Response:
    try:
        await executor.block(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return Response(status_code=200)


@router.post(
    "/users/{user_id}/unblock",
    summary="Разблокировать учётную запись пользователя",
)
async def unblock_user(
        user_id: int,
        executor: FromDishka[BlockUserInteractor],
) -> Response:
    try:
        await executor.unblock(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return Response(status_code=200)