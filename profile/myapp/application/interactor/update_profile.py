from myapp.application.dto.profile import ProfileData, ProfileUpdate
from myapp.application.interface.profile import IProfileUpdater


class UpdateProfileInteractor:
    def __init__(self, updater: IProfileUpdater) -> None:
        self._updater = updater

    async def execute(self, profile_id: int, data: ProfileUpdate) -> ProfileData:
        return await self._updater.update(profile_id, data)
