from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import numpy as np
from sqlalchemy import delete

from app.config import get_settings
from app.infrastructure.db.migrate import run_migrations
from app.infrastructure.db.models import ItemEmbedding
from app.infrastructure.db.session import SyncDatabase
from app.infrastructure.ml.faiss_item_index import FaissItemIndex


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=settings.als_item_embeddings_path)
    parser.add_argument("--skip-db", action="store_true")
    parser.add_argument("--skip-faiss", action="store_true")
    parser.add_argument("--skip-migrations", action="store_true")
    args = parser.parse_args()

    if not args.skip_migrations:
        run_migrations(settings.database_url_sync)

    if not args.input.is_file():
        raise FileNotFoundError(f"Missing {args.input}")

    with args.input.open("rb") as f:
        embeddings: dict[object, np.ndarray] = pickle.load(f)

    if not args.skip_db:
        db = SyncDatabase(settings.database_url_sync)
        rows = [
            ItemEmbedding(
                item_id=str(item_id),
                embedding=vector.astype(float).tolist(),
            )
            for item_id, vector in embeddings.items()
        ]
        with db.session_factory() as session:
            session.execute(delete(ItemEmbedding))
            session.add_all(rows)
            session.commit()
        print(f"item_embeddings table: {len(rows)} rows")

    if not args.skip_faiss:
        index = FaissItemIndex(embeddings)
        index.save(settings.faiss_index_path, settings.faiss_ids_path)
        print(
            f"FAISS index saved to {settings.faiss_index_path}, "
            f"{settings.faiss_ids_path}"
        )


if __name__ == "__main__":
    main()
