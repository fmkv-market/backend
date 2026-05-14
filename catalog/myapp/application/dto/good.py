from pydantic import BaseModel

from myapp.application.dto.base import BaseDTO
from myapp.application.dto.category import CategoryDTO


class GoodItemDTO(BaseDTO):
    id: int
    small_img: str
    title: str
    weight: float
    cost: float
    category: CategoryDTO