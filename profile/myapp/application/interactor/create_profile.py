from myapp.application.dto.profile import ProfileCreate, ProfileData
from myapp.application.exception.profile import ProfileAlreadyExistsException
from myapp.application.interface.profile import IProfileSaver


class CreateProfileInteractor:
    def __init__(self, saver: IProfileSaver) -> None:
        self._saver = saver

    async def execute(self, data: ProfileCreate) -> ProfileData:
        try:
            return await self._saver.save(data)
        except ProfileAlreadyExistsException:
            raise
