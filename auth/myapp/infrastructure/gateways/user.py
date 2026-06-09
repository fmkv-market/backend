from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.user import UserCreate, UserData, UserID
from myapp.application.exception.user import UserEmailNotFoundException
from myapp.application.interface.user import (
    UserSaver,
    UserReader,
    UserReaderEmail,
    UserDeleter,
    UserPasswordUpdater,
    UserBlockManager,
)
from myapp.infrastructure.exceptions.user import UserNotFoundException
from myapp.infrastructure.models.user import UserModel


class UserGateway(UserSaver, UserReaderEmail, UserDeleter, UserPasswordUpdater, UserBlockManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user_create: UserCreate) -> UserData:
        new_user = UserModel(**user_create.model_dump())
        self._session.add(new_user)
        await self._session.commit()
        return UserData.map_to_domain_entity(new_user)

    async def read_one(self, user_id: UserID) -> UserData:
        query = select(UserModel).filter_by(id=user_id)
        result = await self._session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException
        return UserData.map_to_domain_entity(user)

    async def read_by_email(self, email: EmailStr) -> UserData:
        query = select(UserModel).filter_by(email=email)
        result = await self._session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserEmailNotFoundException
        return UserData.map_to_domain_entity(user)

    async def delete(self, user_id: int) -> None:
        query = select(UserModel).filter_by(id=user_id)
        result = await self._session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException
        await self._session.delete(user)
        await self._session.commit()

    async def update_password(self, user_id: int, hash_password: str) -> None:
        query = select(UserModel).filter_by(id=user_id)
        result = await self._session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException
        user.hash_password = hash_password
        await self._session.commit()

    async def set_blocked(self, user_id: int, blocked: bool) -> None:
        query = select(UserModel).filter_by(id=user_id)
        result = await self._session.execute(query)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException
        user.is_blocked = blocked
        await self._session.commit()
