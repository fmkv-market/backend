from myapp.application.dto.user import UserCreate, UserData
from myapp.application.exception.user import UserEmailAlreadyExistsException, UserEmailNotFoundException
from myapp.application.interface.profile_publisher import IProfilePublisher
from myapp.application.interface.register import IRegisterUser
from myapp.application.interface.user import UserSaver, UserReaderEmail


class EmailRegisterUser(IRegisterUser):
    def __init__(
        self,
        saver: UserSaver,
        reader: UserReaderEmail,
        profile_publisher: IProfilePublisher,
    ):
        self._saver = saver
        self._reader = reader
        self._profile_publisher = profile_publisher

    async def register_user(
        self,
        data: UserCreate,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> UserData:
        try:
            user_exists = await self._reader.read_by_email(email=data.email)
            if user_exists:
                raise UserEmailAlreadyExistsException
        except UserEmailNotFoundException:
            pass
        user = await self._saver.save(data)
        await self._profile_publisher.publish_user_created(user.id, first_name, last_name)
        return user
