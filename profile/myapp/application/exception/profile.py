from myapp.application.exception.base import ObjectNotFoundException, ObjectAlreadyExistsException


class ProfileNotFoundException(ObjectNotFoundException):
    detail = "Профиль не найден"


class ProfileAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Профиль уже существует"
