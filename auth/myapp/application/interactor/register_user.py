from myapp.application.dto.user import UserCreate, UserData
from myapp.application.interface.register import IRegisterUser
from myapp.application.interface.user import UserSaver, UserReaderEmail
from myapp.application.exception.user import UserEmailAlreadyExistsException, UserEmailNotFoundException


class EmailRegisterUser(IRegisterUser):
    def __init__(self, saver: UserSaver, reader: UserReaderEmail):
        self._saver = saver
        self._reader = reader

    async def register_user(self, data: UserCreate) -> UserData:
        try:
            user_exists = await self._reader.read_by_email(email=data.email)
            if user_exists:
                raise UserEmailAlreadyExistsException
        except UserEmailNotFoundException:
            pass
        return await self._saver.save(data)


