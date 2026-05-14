from myapp.application.dto.good import GoodItemDTO
from myapp.application.exception.category import CategoryNotFoundException
from myapp.application.services.search import SearchService
from myapp.infrastructure.repository.base import BaseRepository
from myapp.infrastructure.repository.category import CategoryRepository
from myapp.infrastructure.repository.good import GoodRepository


class GoodListInteractor:
    def __init__(self, good_repo: GoodRepository, category_repo: CategoryRepository, search_service: SearchService):
        self.good_repo = good_repo
        self.category_repo = category_repo
        self.search_service = search_service

    async def get_by_category(self, category_id: int) -> list[GoodItemDTO]:
        category = self.category_repo.get_one_or_none(id=category_id)
        if not category:
            raise CategoryNotFoundException

        return await self.good_repo.get_filtered(category_id=category_id)

    def get_by_search(self, value: str) -> list[GoodItemDTO]:
        return self.search_service.proceed(value)

    def get_by_suggestion(self, user_id: int) -> list[GoodItemDTO]:
        pass

