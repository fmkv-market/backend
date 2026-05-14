from myapp.application.exception.otp import OTPNotFoundException
from myapp.application.interface.otp import IOTPStorage
from myapp.application.services.otp import OtpService


class VerifyEmail:
    def __init__(self, otp_storage: IOTPStorage, otp_service: OtpService):
        self.otp_storage = otp_storage
        self.otp_service = otp_service

    async def execute(self, email: str) -> bool:
        otp_exists = await self.otp_storage.get(email)
        if not otp_exists:
            raise OTPNotFoundException
        return True
