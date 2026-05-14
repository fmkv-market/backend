class ApplicationException(Exception):
    pass

class ObjectNotFoundException(ApplicationException):
    detail = "Объект не найден"