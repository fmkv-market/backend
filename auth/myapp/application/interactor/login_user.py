from myapp.application.dto.jwt import JWTData, Payload
from myapp.application.dto.user import EmailLogin, EmailVerifyDTO
from myapp.application.exception.otp import OTPNotFoundException
from myapp.application.exception.password import PasswordValidationException
from myapp.application.exception.user import UserEmailNotFoundException, UserBlockedException
from myapp.application.interface.failed_attempts import IFailedAttemptsStorage
from myapp.application.interface.jwt_manager import IJWTManager
from myapp.application.interface.login import ILoginUser
from myapp.application.interface.otp import IOTPStorage
from myapp.application.interface.pass_manager import IPasswordManager
from myapp.application.interface.publisher import IPublisher
from myapp.application.interface.user import UserReaderEmail, UserBlockManager
from myapp.application.services.otp import OtpService

_MAX_FAILED_ATTEMPTS = 5


class EmailLoginUser(ILoginUser):
    def __init__(
        self,
        reader: UserReaderEmail,
        pass_manager: IPasswordManager,
        jwt_manager: IJWTManager,
        publisher: IPublisher,
        otp_service: OtpService,
        otp_storage: IOTPStorage,
        failed_attempts: IFailedAttemptsStorage,
        block_manager: UserBlockManager,
    ):
        self._reader = reader
        self._pass_manager = pass_manager
        self._jwt_manager = jwt_manager
        self._publisher = publisher
        self._otp_service = otp_service
        self._otp_storage = otp_storage
        self._failed_attempts = failed_attempts
        self._block_manager = block_manager

    async def request_login(self, data: EmailLogin):
        user = await self._reader.read_by_email(email=data.email)
        if not user:
            raise UserEmailNotFoundException

        if user.is_blocked:
            raise UserBlockedException

        if not await self._pass_manager.verify_password(data.password, user.hash_password):
            count = await self._failed_attempts.increment(data.email)
            if count >= _MAX_FAILED_ATTEMPTS:
                await self._block_manager.set_blocked(user.id, True)
            raise PasswordValidationException

        await self._failed_attempts.reset(data.email)

        exists_otp = await self._otp_storage.get(email=data.email)
        if not exists_otp:
            otp = self._otp_service.generate_otp()
            await self._otp_storage.set(email=data.email, otp=otp)
            await self._publisher.publish(data.email, otp)

    async def verify_email(self, data: EmailVerifyDTO) -> JWTData:
        exists_otp = await self._otp_storage.get(email=data.email)
        print(2222, exists_otp)
        if not exists_otp:
            raise OTPNotFoundException
        user_exists = await self._reader.read_by_email(email=data.email)
        payload = Payload(id=user_exists.id)
        await self._otp_storage.delete(email=data.email)
        return await self._jwt_manager.create_jwt(payload)



