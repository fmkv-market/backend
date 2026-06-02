from abc import ABC, abstractmethod
from typing import Any


FeatureVector = dict[str, Any]


class IUserFeaturesRepository(ABC):
    @abstractmethod
    def get_user_features(self, user_id: str) -> FeatureVector | None:
        pass


class IItemFeaturesRepository(ABC):
    @abstractmethod
    def get_item_features(self, item_id: str) -> FeatureVector | None:
        pass


class IUserItemFeaturesRepository(ABC):
    @abstractmethod
    def get_user_item_features(
        self, user_id: str, item_id: str
    ) -> FeatureVector | None:
        pass
