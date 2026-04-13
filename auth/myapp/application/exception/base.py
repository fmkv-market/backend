class ApplicationException(Exception):
    pass

class ObjectNotFoundException(ApplicationException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(ApplicationException):
    detail = "Объект уже существует"