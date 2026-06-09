from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations(database_url_sync: str, alembic_ini: Path | None = None) -> None:
    ini_path = alembic_ini or Path(__file__).resolve().parents[3] / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("sqlalchemy.url", database_url_sync)
    command.upgrade(cfg, "head")
