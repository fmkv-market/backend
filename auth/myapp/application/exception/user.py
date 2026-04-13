from myapp.application.exception.base import ObjectNotFoundException
from myapp.infrastructure.exceptions import ObjectAlreadyExistsException


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"

class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class UserEmailAlreadyExistsException(UserAlreadyExistsException):
    detail = "Пользователь с таким email уже существует"

class UserEmailNotFoundException(UserNotFoundException):
    detail = "Пользователя с таким email не существует"