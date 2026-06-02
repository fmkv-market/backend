from typing import Any

from app.core.interfaces.repositories.features import FeatureVector


def orm_to_feature_vector(entity: Any, keys: list[str]) -> FeatureVector:
    return {key: getattr(entity, key) for key in keys}
