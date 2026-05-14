from typing import Protocol

from myapp.application.dto.good import GoodItemDTO


class GoodListReader(Protocol):
    def get_by_category(self, category_id: int) -> list[GoodItemDTO]: ...

    def get_by_search(self, value: str) -> list[GoodItemDTO]: ...

    def get_by_suggestion(self, user_id: int) -> list[GoodItemDTO]: ...

