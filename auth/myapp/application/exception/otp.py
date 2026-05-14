from myapp.application.exception.base import ObjectNotFoundException


class OTPNotFoundException(ObjectNotFoundException):
    detail = "OTP для данного email не существует"