from myapp.application.exception.base import ApplicationException


class JWTDecodeException(ApplicationException):
    detail = "Неверный токен"