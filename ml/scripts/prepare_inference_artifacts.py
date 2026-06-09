"""
Export inference artifacts from training outputs (notebooks ALS.ipynb / Ranking.ipynb).

Usage:
  python -m scripts.prepare_inference_artifacts \\
    --embeddings-dir /path/to/als_pickles \\
    --features-parquet /path/to/train_with_features.parquet \\
    --interactions-parquet /path/to/train_pos_interactions.parquet \\
    --ranker-model /path/to/ranker.cbm \\
    --output-dir artifacts
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import polars as pl

from app.core.constants import (
    ITEM_FEATURE_KEYS,
    USER_FEATURE_KEYS,
    USER_ITEM_FEATURE_KEYS,
)


def export_features(source: Path, output_dir: Path) -> None:
    df = pl.read_parquet(source)

    user_df = (
        df.sort("timestamp")
        .group_by("user_id")
        .agg([pl.col(c).last() for c in USER_FEATURE_KEYS])
    )
    user_df.write_parquet(output_dir / "user_features.parquet")

    item_df = (
        df.sort("timestamp")
        .group_by("item_id")
        .agg([pl.col(c).last() for c in ITEM_FEATURE_KEYS])
    )
    item_df.write_parquet(output_dir / "item_features.parquet")

    u2i_df = (
        df.sort("timestamp")
        .group_by(["user_id", "item_id"])
        .agg([pl.col(c).last() for c in USER_ITEM_FEATURE_KEYS])
    )
    u2i_df.write_parquet(output_dir / "user_item_features.parquet")


def export_catalog(interactions: Path, output_dir: Path) -> None:
    df = pl.read_parquet(interactions)
    catalog = (
        df.sort("timestamp")
        .group_by("item_id")
        .agg(pl.col("product_category").last().alias("product_category"))
    )
    catalog.write_parquet(output_dir / "item_catalog.parquet")

    popular = (
        df.group_by("item_id")
        .agg(pl.len().alias("cnt"))
        .sort("cnt", descending=True)
        .head(200)["item_id"]
        .to_list()
    )
    with (output_dir / "popular_items.json").open("w", encoding="utf-8") as f:
        json.dump(popular, f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--embeddings-dir", type=Path, required=True)
    parser.add_argument("--features-parquet", type=Path, required=True)
    parser.add_argument("--interactions-parquet", type=Path, required=True)
    parser.add_argument("--ranker-model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        args.embeddings_dir / "als_user_embeddings.pkl",
        args.output_dir / "als_user_embeddings.pkl",
    )
    shutil.copy2(
        args.embeddings_dir / "als_item_embeddings.pkl",
        args.output_dir / "als_item_embeddings.pkl",
    )
    shutil.copy2(args.ranker_model, args.output_dir / "ranker.cbm")

    export_features(args.features_parquet, args.output_dir)
    export_catalog(args.interactions_parquet, args.output_dir)
    print(f"Artifacts written to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
