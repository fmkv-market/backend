from myapp.application.dto.profile import ProfileData
from myapp.application.interface.profile import IProfileReader


class GetProfileInteractor:
    def __init__(self, reader: IProfileReader) -> None:
        self._reader = reader

    async def by_user_id(self, user_id: int) -> ProfileData:
        return await self._reader.read_by_user_id(user_id)

    async def by_profile_id(self, profile_id: int) -> ProfileData:
        return await self._reader.read_one(profile_id)
