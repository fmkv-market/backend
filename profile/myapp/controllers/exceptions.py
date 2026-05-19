from fastapi import HTTPException


class ProfileHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ProfileNotFoundHTTPException(ProfileHTTPException):
    status_code = 404
    detail = "Профиль не найден"


class ProfileAlreadyExistsHTTPException(ProfileHTTPException):
    status_code = 409
    detail = "Профиль уже существует"


class AddressNotFoundHTTPException(ProfileHTTPException):
    status_code = 404
    detail = "Адрес не найден"
