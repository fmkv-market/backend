from __future__ import annotations

from myapp.application.dto.base import BaseDTO


class CategoryDTO(BaseDTO):
    parent: None | CategoryDTO = None
    value: str
    is_leaf: bool


