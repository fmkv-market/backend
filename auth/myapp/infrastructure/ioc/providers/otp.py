from dishka import Provider, provide, Scope

from myapp.application.interface.otp import IOTPStorage
from myapp.application.services.otp import OtpService
from myapp.infrastructure.gateways.otp import OTPRedisStorage


class OTPProvider(Provider):
    otp_storage = provide(
        OTPRedisStorage,
        scope=Scope.APP,
        provides=IOTPStorage
    )
    otp_service = provide(
        OtpService,
        scope=Scope.APP,
    )
