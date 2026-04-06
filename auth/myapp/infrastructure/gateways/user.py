from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.user import UserCreate, UserData
from myapp.application.interface.user import UserSaver, UserReader
from myapp.infrastructure.models.user import UserModel


class UserGateway(UserSaver, UserReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user_create: UserCreate) -> UserData:
        new_user = UserModel(**user_create.model_dump())
        self._session.add(new_user)
        await self._session.commit()
        return UserData.model_validate(new_user)

