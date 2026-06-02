"""
Полная загрузка данных
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def _run(module: str, extra: list[str] | None = None) -> None:
    cmd = [sys.executable, "-m", module, *(extra or [])]
    print(f"\n>>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-migrations", action="store_true")
    parser.add_argument("--skip-features", action="store_true")
    parser.add_argument("--skip-users", action="store_true")
    parser.add_argument("--skip-items", action="store_true")
    args = parser.parse_args()

    mig_extra = ["--skip-migrations"] if args.skip_migrations else []

    if not args.skip_features:
        _run("scripts.load_features_to_postgres", mig_extra)

    if not args.skip_users:
        _run("scripts.load_user_embeddings_to_redis")

    if not args.skip_items:
        item_extra = ["--skip-migrations"] if args.skip_migrations else []
        _run("scripts.load_item_embeddings", item_extra)

    print("\nAll loaders finished.")


if __name__ == "__main__":
    main()
