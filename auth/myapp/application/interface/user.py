from typing import Protocol

from pydantic import EmailStr

from myapp.application.dto.user import UserID, UserCreate, UserData


class UserSaver(Protocol):
    async def save(self, user_create: UserCreate) -> UserData: ...


class UserReader(Protocol):
    async def read_one(self, user_id: UserID) -> UserData: ...


class UserReaderEmail(UserReader):
    async def read_by_email(self, email: EmailStr) -> UserData: ...


class UserDeleter(Protocol):
    async def delete(self, user_id: int) -> None: ...


class UserPasswordUpdater(Protocol):
    async def update_password(self, user_id: int, hash_password: str) -> None: ...


class UserBlockManager(Protocol):
    async def set_blocked(self, user_id: int, blocked: bool) -> None: ...
