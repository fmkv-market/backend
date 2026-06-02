from pathlib import Path
from typing import Any

import polars as pl

from app.core.interfaces.repositories.features import (
    FeatureVector,
    IItemFeaturesRepository,
    IUserFeaturesRepository,
    IUserItemFeaturesRepository,
)


def _row_to_dict(row: dict[str, Any], columns: list[str]) -> FeatureVector:
    return {col: row[col] for col in columns if col in row}


class FileUserFeaturesRepository(IUserFeaturesRepository):
    def __init__(self, path: Path, feature_columns: list[str]) -> None:
        df = pl.read_parquet(path)
        self._index: dict[int, FeatureVector] = {}
        for row in df.iter_rows(named=True):
            self._index[int(row["user_id"])] = _row_to_dict(row, feature_columns)

    def get_user_features(self, user_id: int) -> FeatureVector | None:
        return self._index.get(user_id)


class FileItemFeaturesRepository(IItemFeaturesRepository):
    def __init__(self, path: Path, feature_columns: list[str]) -> None:
        df = pl.read_parquet(path)
        self._index: dict[int, FeatureVector] = {}
        for row in df.iter_rows(named=True):
            self._index[int(row["item_id"])] = _row_to_dict(row, feature_columns)

    def get_item_features(self, item_id: int) -> FeatureVector | None:
        return self._index.get(item_id)


class FileUserItemFeaturesRepository(IUserItemFeaturesRepository):
    def __init__(self, path: Path, feature_columns: list[str]) -> None:
        df = pl.read_parquet(path)
        self._index: dict[tuple[int, int], FeatureVector] = {}
        for row in df.iter_rows(named=True):
            key = (int(row["user_id"]), int(row["item_id"]))
            self._index[key] = _row_to_dict(row, feature_columns)

    def get_user_item_features(self, user_id: int, item_id: int) -> FeatureVector | None:
        return self._index.get((user_id, item_id))
