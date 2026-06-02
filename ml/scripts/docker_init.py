"""
Одноразовая инициализация в Docker: миграции + загрузка данных.

"""

from __future__ import annotations

import subprocess
import sys

from pathlib import Path

from app.config import get_settings
from app.infrastructure.db.migrate import run_migrations


def _require_files(paths: list[Path]) -> None:
    missing = [p for p in paths if not p.is_file()]
    if missing:
        lines = "\n  ".join(str(p) for p in missing)
        raise FileNotFoundError(
            "Missing required files. Check paths in .env and mount ./data, ./artifacts:\n  "
            + lines
        )


def main() -> None:
    settings = get_settings()
    _require_files(
        [
            settings.als_user_embeddings_path,
            settings.als_item_embeddings_path,
            settings.user_features_path,
            settings.item_features_path,
            settings.user_item_features_path,
            settings.item_catalog_path,
            settings.ranker_model_path,
        ]
    )

    print(">>> Alembic migrations")
    run_migrations(settings.database_url_sync)

    print(">>> Load data (Postgres, Redis, FAISS)")
    subprocess.run(
        [sys.executable, "-m", "scripts.load_all", "--skip-migrations"],
        check=True,
    )

    print(">>> Docker init completed")


if __name__ == "__main__":
    main()
