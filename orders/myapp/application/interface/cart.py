from abc import ABC, abstractmethod

from myapp.application.dto.base import BaseDTO
from myapp.application.dto.cart import CartDTO
from myapp.application.entity.cart import Cart


class CartSaver(ABC):
    @abstractmethod
    async def save(self, cart: Cart):
        raise NotImplementedError


class CartReader(ABC):
    @abstractmethod
    async def read_by_id(self, cart_id: int) -> CartDTO:
        raise NotImplementedError

    @abstractmethod
    async def read_by_user_id(self, user_id: str) -> CartDTO:
        raise NotImplementedError


class CartUpdater(ABC):
    @abstractmethod
    async def add_item(self, cart_id: int, data: BaseDTO) -> CartDTO:
        raise NotImplementedError

    @abstractmethod
    async def remove_item(self, cart_id: int, data: BaseDTO) -> None:
        raise NotImplementedError