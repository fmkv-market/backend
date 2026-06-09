from myapp.application.exception.password import PasswordValidationException
from myapp.application.interface.pass_manager import IPasswordManager
from myapp.application.interface.profile_publisher import IProfilePublisher
from myapp.application.interface.user import UserReaderEmail, UserDeleter


class DeleteUserInteractor:
    def __init__(
        self,
        reader: UserReaderEmail,
        deleter: UserDeleter,
        pass_manager: IPasswordManager,
        profile_publisher: IProfilePublisher,
    ) -> None:
        self._reader = reader
        self._deleter = deleter
        self._pass_manager = pass_manager
        self._profile_publisher = profile_publisher

    async def execute(self, email: str, password: str) -> None:
        user = await self._reader.read_by_email(email=email)
        if not await self._pass_manager.verify_password(password, user.hash_password):
            raise PasswordValidationException
        await self._deleter.delete(user.id)
        await self._profile_publisher.publish_user_deleted(user.id)