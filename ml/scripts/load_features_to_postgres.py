from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl
from sqlalchemy import delete

from app.config import get_settings
from app.infrastructure.db.models import (
    ItemCatalog,
    ItemFeatures,
    UserFeatures,
    UserItemFeatures,
)
from app.infrastructure.db.migrate import run_migrations
from app.infrastructure.db.session import SyncDatabase


def _load_table(session, model, path: Path, batch_size: int = 500) -> None:
    """Загрузка с batch-обработкой для экономии памяти"""
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}")

    print(f"Loading {model.__tablename__} from {path}")

    session.execute(delete(model))
    session.commit()

    total_rows = 0

    df = pl.read_parquet(path)

    if model == UserFeatures or model == UserItemFeatures:
        df = df.with_columns(pl.col("user_id").cast(pl.Utf8))
    if model == ItemFeatures or model == UserItemFeatures or model == ItemCatalog:
        if "item_id" in df.columns:
            df = df.with_columns(pl.col("item_id").cast(pl.Utf8))

    for i in range(0, len(df), batch_size):
        batch_df = df.slice(i, batch_size)
        rows = [model(**row) for row in batch_df.iter_rows(named=True)]
        session.add_all(rows)
        session.commit()
        total_rows += len(rows)
        print(f"  Loaded {total_rows} rows...")

    print(f"{model.__tablename__}: {total_rows} rows")


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=settings.data_dir)
    parser.add_argument("--skip-migrations", action="store_true")
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    if not args.skip_migrations:
        run_migrations(settings.database_url_sync)

    db = SyncDatabase(settings.database_url_sync)
    data = args.data_dir

    with db.session_factory() as session:
        _load_table(session, UserFeatures, data / "user_features.parquet", args.batch_size)
        _load_table(session, ItemFeatures, data / "item_features.parquet", args.batch_size)
        _load_table(session, UserItemFeatures, data / "user_item_features.parquet", args.batch_size)
        _load_table(session, ItemCatalog, data / "item_catalog.parquet", args.batch_size)
        session.commit()

    print("Done.")


if __name__ == "__main__":
    main()
