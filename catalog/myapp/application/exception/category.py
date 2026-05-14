from myapp.application.exception.base import ObjectNotFoundException


class CategoryNotFoundException(ObjectNotFoundException):
    detail = "Категория не найден"