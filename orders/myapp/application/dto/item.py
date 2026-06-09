from myapp.application.dto.base import BaseDTO


class ItemInfoDTO(BaseDTO):
    item_id: int
    cost: float
    quantity: int = 1