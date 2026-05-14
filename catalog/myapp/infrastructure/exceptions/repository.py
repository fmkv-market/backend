from myapp.infrastructure.exceptions.base import InfraException


class ObjectNotFoundException(InfraException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(InfraException):
    detail = "Объект уже существует"