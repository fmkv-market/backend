from myapp.application.interface.pass_manager import IPasswordManager
from myapp.application.interface.user import UserPasswordUpdater


class AdminChangePasswordInteractor:
    """Принудительная смена пароля администратором (при подозрении на взлом)."""

    def __init__(
        self,
        updater: UserPasswordUpdater,
        pass_manager: IPasswordManager,
    ) -> None:
        self._updater = updater
        self._pass_manager = pass_manager

    async def execute(self, user_id: int, new_password: str) -> None:
        hashed_password = await self._pass_manager.hash_password(new_password)
        await self._updater.update_password(user_id, hashed_password)