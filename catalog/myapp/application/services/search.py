from myapp.application.dto.good import GoodItemDTO


class SearchService:
    def __init__(self):
        ...

    def proceed(self, value: str, is_partial: bool = False) -> list[GoodItemDTO]:
        if is_partial:
            return self._partial_search(value)
        return self._exact_search(value)

    def _partial_search(self, value: str) -> list[GoodItemDTO]:
        ...

    def _exact_search(self, value: str) -> list[GoodItemDTO]:
        ...

