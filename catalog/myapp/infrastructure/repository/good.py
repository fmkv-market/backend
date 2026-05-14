from myapp.application.dto.base import BaseDTO
from myapp.application.dto.good import GoodItemDTO
from myapp.infrastructure.models import Goods
from myapp.infrastructure.repository.base import BaseRepository


class GoodRepository(BaseRepository):
    model = Goods
    dto: BaseDTO = GoodItemDTO
