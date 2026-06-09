from sqlalchemy.orm import Session, sessionmaker

from app.core.constants import (
    ITEM_FEATURE_KEYS,
    USER_FEATURE_KEYS,
    USER_ITEM_FEATURE_KEYS,
)
from app.core.interfaces.repositories.features import (
    FeatureVector,
    IItemFeaturesRepository,
    IUserFeaturesRepository,
    IUserItemFeaturesRepository,
)
from app.infrastructure.db.mappers import orm_to_feature_vector
from app.infrastructure.db.models import ItemFeatures, UserFeatures, UserItemFeatures


class PostgresUserFeaturesRepository(IUserFeaturesRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def get_user_features(self, user_id: int) -> FeatureVector | None:
        with self._session_factory() as session:
            entity = session.get(UserFeatures, user_id)
        if entity is None:
            return None
        return orm_to_feature_vector(entity, USER_FEATURE_KEYS)


class PostgresItemFeaturesRepository(IItemFeaturesRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def get_item_features(self, item_id: int) -> FeatureVector | None:
        with self._session_factory() as session:
            entity = session.get(ItemFeatures, item_id)
        if entity is None:
            return None
        return orm_to_feature_vector(entity, ITEM_FEATURE_KEYS)


class PostgresUserItemFeaturesRepository(IUserItemFeaturesRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def get_user_item_features(self, user_id: int, item_id: int) -> FeatureVector | None:
        with self._session_factory() as session:
            entity = session.get(UserItemFeatures, (user_id, item_id))
        if entity is None:
            return None
        return orm_to_feature_vector(entity, USER_ITEM_FEATURE_KEYS)
