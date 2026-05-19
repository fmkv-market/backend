from typing import Protocol

from myapp.application.dto.profile import ProfileCreate, ProfileData, ProfileUpdate


class IProfileSaver(Protocol):
    async def save(self, data: ProfileCreate) -> ProfileData: ...


class IProfileReader(Protocol):
    async def read_by_user_id(self, user_id: int) -> ProfileData: ...
    async def read_one(self, profile_id: int) -> ProfileData: ...


class IProfileUpdater(Protocol):
    async def update(self, profile_id: int, data: ProfileUpdate) -> ProfileData: ...
