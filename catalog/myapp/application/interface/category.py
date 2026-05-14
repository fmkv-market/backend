from typing import Protocol

from myapp.application.dto.category import CategoryDTO
from myapp.application.dto.good import GoodItemDTO


class CategoryReader(Protocol):
    def get_parent_categories(self) -> list[CategoryDTO]: ...

    def get_all_categories(self) -> list[CategoryDTO]: ...

    def get_children(self, category_id: int) -> list[CategoryDTO]: ...
