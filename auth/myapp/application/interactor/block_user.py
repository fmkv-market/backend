from myapp.application.interface.user import UserBlockManager, UserReaderEmail
from myapp.application.exception.user import UserBlockedException


_MAX_FAILED_ATTEMPTS = 5
_BLOCK_KEY = "failed_login:{email}"


class BlockUserInteractor:
    def __init__(self, block_manager: UserBlockManager) -> None:
        self._block_manager = block_manager

    async def block(self, user_id: int) -> None:
        await self._block_manager.set_blocked(user_id, True)

    async def unblock(self, user_id: int) -> None:
        await self._block_manager.set_blocked(user_id, False)