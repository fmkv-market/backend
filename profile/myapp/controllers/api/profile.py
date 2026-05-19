from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from myapp.application.dto.profile import ProfileUpdate
from myapp.application.exception.profile import ProfileNotFoundException
from myapp.application.interactor.get_profile import GetProfileInteractor
from myapp.application.interactor.update_profile import UpdateProfileInteractor
from myapp.controllers.exceptions import ProfileNotFoundHTTPException
from myapp.controllers.schemas.profile import ProfileUpdateRequest, ProfileResponse

router = APIRouter(prefix="/profile", tags=["Профиль"], route_class=DishkaRoute)


@router.get("/{user_id}", summary="Получить профиль пользователя")
async def get_profile(
    user_id: int,
    interactor: FromDishka[GetProfileInteractor],
) -> ProfileResponse:
    try:
        profile = await interactor.by_user_id(user_id)
    except ProfileNotFoundException:
        raise ProfileNotFoundHTTPException
    return ProfileResponse.model_validate(profile.model_dump())


@router.put("/{user_id}", summary="Обновить профиль пользователя")
async def update_profile(
    user_id: int,
    data: ProfileUpdateRequest,
    get_interactor: FromDishka[GetProfileInteractor],
    update_interactor: FromDishka[UpdateProfileInteractor],
) -> ProfileResponse:
    try:
        profile = await get_interactor.by_user_id(user_id)
    except ProfileNotFoundException:
        raise ProfileNotFoundHTTPException
    update_dto = ProfileUpdate(**data.model_dump(exclude_none=True))
    updated = await update_interactor.execute(profile.id, update_dto)
    return ProfileResponse.model_validate(updated.model_dump())
