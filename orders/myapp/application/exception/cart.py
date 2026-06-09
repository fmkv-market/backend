from myapp.application.exception.base import ApplicationException


class CoreCartException(ApplicationException):
    pass

class CarQuantityMustBePositive(CoreCartException):
    detail = "Количество элементов в корзине не может быть отрицательным"

class SuchItemNotInCart(CoreCartException):
    detail = "Текущего товара нет в корзине"

class CarQuantityTooMuch(CoreCartException):
    detail = "Слишком большое количество элементов в корзине"

class CarTotalMustBePositive(CoreCartException):
    detail = "Общая стоимость корзины не может быть отрицательной"