from myapp.application.dto.base import BaseDTO


class CreateCartDTO(BaseDTO):
    user_id: int


class CartDTO(BaseDTO):
    id: int
    user_id: int
    total: int
    quantity: int
