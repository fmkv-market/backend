from myapp.application.exception.base import ApplicationException


class PasswordValidationException(ApplicationException):
    detail = "Неправильный пароль"