from abc import ABC, abstractmethod

from myapp.application.dto.base import BaseDTO


class ILoginUser(ABC):
    @abstractmethod
    def login_user(self, data: BaseDTO):
        raise NotImplementedError