from fastapi import HTTPException


class AuthHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserEmailAlreadyExistsHTTPException(AuthHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserEmailNotExistsHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Пользователь с такой почтой не найден"


class IncorrectPasswordHTTPException(AuthHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class UserNotFoundHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class UserBlockedHTTPException(AuthHTTPException):
    status_code = 403
    detail = "Учётная запись заблокирована"

class OTPInvalidHTTPException(AuthHTTPException):
    status_code = 400