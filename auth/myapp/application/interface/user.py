from typing import Protocol

from myapp.application.dto.user import UserID, UserCreate, UserData


class UserSaver(Protocol):
    async def save(self, user_create: UserCreate) -> UserData: ...


class UserReader(Protocol):
    async def read_one(self, user_id: UserID) -> UserData: ...

