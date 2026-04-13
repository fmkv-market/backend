from myapp.application.dto.jwt import JWTData, Payload
from myapp.application.dto.user import EmailLogin
from myapp.application.exception.password import PasswordValidationException
from myapp.application.interface.jwt_manager import IJWTManager
from myapp.application.interface.login import ILoginUser
from myapp.application.interface.pass_manager import IPasswordManager
from myapp.application.interface.user import UserReaderEmail
from myapp.application.exception.user import UserEmailNotFoundException


class EmailLoginUser(ILoginUser):
    def __init__(self, reader: UserReaderEmail, pass_manager: IPasswordManager, jwt_manager: IJWTManager):
        self._reader = reader
        self._pass_manager = pass_manager
        self._jwt_manager = jwt_manager

    async def login_user(self, data: EmailLogin) -> JWTData:
        user_exists = await self._reader.read_by_email(email=data.email)
        if not user_exists:
            raise UserEmailNotFoundException
        if not self._pass_manager.verify_password(data.password, user_exists.hash_password):
            raise PasswordValidationException
        payload = Payload(id=user_exists.id)

        return await self._jwt_manager.create_jwt(payload)



