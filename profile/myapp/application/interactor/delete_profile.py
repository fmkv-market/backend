from myapp.application.interface.profile import IProfileDeleter


class DeleteProfileInteractor:
    def __init__(self, deleter: IProfileDeleter) -> None:
        self._deleter = deleter

    async def by_user_id(self, user_id: int) -> None:
        await self._deleter.delete_by_user_id(user_id)