from abc import ABC, abstractmethod

from myapp.application.dto.base import BaseDTO


class IRegisterUser(ABC):
    @abstractmethod
    def register_user(self, data: BaseDTO):
        raise NotImplementedError