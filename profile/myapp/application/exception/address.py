from myapp.application.exception.base import ObjectNotFoundException


class AddressNotFoundException(ObjectNotFoundException):
    detail = "Адрес не найден"
