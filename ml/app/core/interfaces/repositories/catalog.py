from abc import ABC, abstractmethod


class IItemCatalogRepository(ABC):
    @abstractmethod
    def get_product_category(self, item_id: str) -> str | None:
        pass


class IPopularItemsRepository(ABC):
    @abstractmethod
    def get_popular_items(self, n: int) -> list[str]:
        pass
