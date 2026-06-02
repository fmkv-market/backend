from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str
    debug: bool

    data_dir: Path

    als_user_embeddings_path: Path
    als_item_embeddings_path: Path
    als_mappers_path: Path

    faiss_index_path: Path
    faiss_ids_path: Path
    prefer_saved_faiss_index: bool

    ranker_model_path: Path
    user_features_path: Path
    item_features_path: Path
    user_item_features_path: Path
    item_catalog_path: Path

    default_candidates: int
    default_top_k: int
    fill_value: float

    redis_host: str
    redis_port: int
    redis_db: int
    redis_pass: str
    redis_user_embedding_key_prefix: str

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    repository_backend: str
    run_migrations_on_startup: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def faiss_files_exist(self) -> bool:
        return self.faiss_index_path.is_file() and self.faiss_ids_path.is_file()


@lru_cache
def get_settings() -> Settings:
    return Settings()
