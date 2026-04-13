from myapp.infrastructure.exceptions.base import InfraException


class UserNotFoundException(InfraException):
    detail = "Пользователь не найден"

