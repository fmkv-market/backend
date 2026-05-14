from myapp.application.dto.base import BaseDTO
from myapp.application.dto.category import CategoryDTO
from myapp.infrastructure.models import Categories
from myapp.infrastructure.repository.base import BaseRepository


class CategoryRepository(BaseRepository):
    model = Categories
    dto: BaseDTO = CategoryDTO