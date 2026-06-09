from pathlib import Path

import numpy as np
from catboost import CatBoostRanker, Pool

from app.config import Settings
from app.core.constants import (
    CAT_FEATURE_COLUMNS,
    FEATURE_COLUMNS,
    ITEM_FEATURE_KEYS,
    USER_FEATURE_KEYS,
    USER_ITEM_FEATURE_KEYS,
)
from app.core.interfaces.ranker import IRanker
from app.core.interfaces.repositories.catalog import IItemCatalogRepository
from app.core.interfaces.repositories.features import (
    IItemFeaturesRepository,
    IUserFeaturesRepository,
    IUserItemFeaturesRepository,
)
from app.domain.entities import Candidate, RankedItem


class CatBoostRankerModel(IRanker):
    def __init__(
        self,
        model_path: Path,
        user_features: IUserFeaturesRepository,
        item_features: IItemFeaturesRepository,
        user_item_features: IUserItemFeaturesRepository,
        item_catalog: IItemCatalogRepository,
        settings: Settings,
    ) -> None:
        self._model = CatBoostRanker()
        self._model.load_model(str(model_path))
        self._user_features = user_features
        self._item_features = item_features
        self._user_item_features = user_item_features
        self._item_catalog = item_catalog
        self._fill_value = settings.fill_value

    def rank(
        self,
        user_id: str,
        candidates: list[Candidate],
        top_k: int,
    ) -> list[RankedItem]:
        if not candidates:
            return []

        matrix, group_id = self._build_feature_matrix(user_id, candidates)
        pool = Pool(
            matrix,
            feature_names=FEATURE_COLUMNS,
            cat_features=CAT_FEATURE_COLUMNS,
            group_id=group_id,
        )
        scores = self._model.predict(pool)

        order = np.argsort(-np.asarray(scores, dtype=np.float64))
        ranked: list[RankedItem] = []
        for rank, idx in enumerate(order[:top_k], start=1):
            ranked.append(
                RankedItem(
                    item_id=candidates[idx].item_id,
                    score=float(scores[idx]),
                    rank=rank,
                )
            )
        return ranked

    def _build_feature_matrix(
        self,
        user_id: str,
        candidates: list[Candidate],
    ) -> tuple[np.ndarray, list[str]]:
        user_feats = self._user_features.get_user_features(user_id) or {}
        rows: list[list[float | str]] = []
        group_id = str(user_id)

        for candidate in candidates:
            item_feats = self._item_features.get_item_features(candidate.item_id) or {}
            u2i_feats = (
                self._user_item_features.get_user_item_features(
                    user_id, candidate.item_id
                )
                or {}
            )
            category = self._item_catalog.get_product_category(candidate.item_id)
            if category is None:
                category = "unknown"

            row: list[float | str] = []
            for key in USER_FEATURE_KEYS:
                row.append(float(user_feats.get(key, self._fill_value)))
            for key in ITEM_FEATURE_KEYS:
                row.append(float(item_feats.get(key, self._fill_value)))
            for key in USER_ITEM_FEATURE_KEYS:
                row.append(float(u2i_feats.get(key, self._fill_value)))
            row.append(category)
            rows.append(row)

        return np.array(rows, dtype=object), [group_id] * len(candidates)
