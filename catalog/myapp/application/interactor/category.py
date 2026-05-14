from typing import Protocol
from unicodedata import category

from myapp.application.dto.category import CategoryDTO
from myapp.application.dto.good import GoodItemDTO
from myapp.application.exception.category import CategoryNotFoundException
from myapp.application.services.search import SearchService
from myapp.infrastructure.repository.base import BaseRepository
from myapp.infrastructure.repository.category import CategoryRepository


class CategoryListInteractor:
    def __init__(self, category_repo: CategoryRepository, search_service: SearchService):
        self.category_repo = category_repo
        self.search_service = search_service

    async def get_all_categories(self) -> list[CategoryDTO]:
        return await self.category_repo.get_all()

    async def get_parent_categories(self) -> list[CategoryDTO]:
        return await self.category_repo.get_all(parent=None)

    async def get_children(self, category_id: int) -> list[CategoryDTO]:
        parent_category = await self.category_repo.get_one_or_none(id=category_id)
        if not parent_category:
            raise CategoryNotFoundException
        return await self.category_repo.get_filtered(parent_id=parent_category.id)
