import json
from pathlib import Path

import polars as pl

from app.core.interfaces.repositories.catalog import (
    IItemCatalogRepository,
    IPopularItemsRepository,
)


class FileItemCatalogRepository(IItemCatalogRepository):
    def __init__(self, path: Path) -> None:
        df = pl.read_parquet(path)
        self._categories: dict[int, str] = {}
        for row in df.iter_rows(named=True):
            self._categories[int(row["item_id"])] = str(row["product_category"])

    def get_product_category(self, item_id: int) -> str | None:
        return self._categories.get(item_id)


class FilePopularItemsRepository(IPopularItemsRepository):
    def __init__(self, path: Path, item_catalog_path: Path | None = None) -> None:
        if path.exists():
            with path.open(encoding="utf-8") as f:
                self._items: list[int] = json.load(f)
            return

        if item_catalog_path is None or not item_catalog_path.exists():
            self._items = []
            return

        df = pl.read_parquet(item_catalog_path)
        self._items = df["item_id"].head(200).cast(pl.Int64).to_list()

    def get_popular_items(self, n: int) -> list[int]:
        return self._items[:n]
