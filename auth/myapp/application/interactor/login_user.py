from myapp.application.dto.user import UserCreate, UserData, EmailLogin
from myapp.application.interface.login import ILoginUser
from myapp.application.interface.register import IRegisterUser
from myapp.application.interface.user import UserSaver, UserReaderEmail
from myapp.application.exception.user import UserEmailAlreadyExistsException, UserEmailNotFoundException


class EmailLoginUser(ILoginUser):
    def __init__(self, reader: UserReaderEmail):
        self._reader = reader

    async def login_user(self, data: EmailLogin) -> UserData:
        user_exists = await self._reader.read_by_email(email=data.email)
        if not user_exists:
            raise UserEmailNotFoundException

