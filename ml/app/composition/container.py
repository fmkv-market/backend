from dataclasses import dataclass

import redis

from app.config import Settings, get_settings
from app.core.constants import (
    ITEM_FEATURE_KEYS,
    USER_FEATURE_KEYS,
    USER_ITEM_FEATURE_KEYS,
)
from app.core.interfaces.candidate_generator import ICandidateGenerator
from app.core.interfaces.ranker import IRanker
from app.core.interfaces.repositories.catalog import IItemCatalogRepository
from app.core.interfaces.repositories.features import (
    IItemFeaturesRepository,
    IUserFeaturesRepository,
    IUserItemFeaturesRepository,
)
from app.core.interfaces.repositories.item_index import IItemCandidateIndex
from app.core.services.recommendation_service import RecommendationService
from app.infrastructure.db.migrate import run_migrations
from app.infrastructure.db.session import SyncDatabase, create_sync_database
from app.infrastructure.ml.catboost_ranker import CatBoostRankerModel
from app.infrastructure.ml.dot_product_knn import IALSCandidateGenerator
from app.infrastructure.ml.faiss_item_index import FaissItemIndex
from app.infrastructure.redis.client import create_redis_client
from app.infrastructure.repositories.file_catalog_repository import (
    FileItemCatalogRepository,
)
from app.infrastructure.repositories.file_features_repository import (
    FileItemFeaturesRepository,
    FileUserFeaturesRepository,
    FileUserItemFeaturesRepository,
)
from app.infrastructure.repositories.postgres_catalog_repository import (
    PostgresItemCatalogRepository,
)
from app.infrastructure.repositories.postgres_features_repository import (
    PostgresItemFeaturesRepository,
    PostgresUserFeaturesRepository,
    PostgresUserItemFeaturesRepository,
)
from app.infrastructure.repositories.redis_user_embedding_repository import (
    RedisUserEmbeddingRepository,
)


@dataclass
class AppContainer:
    settings: Settings
    recommendation_service: RecommendationService
    sync_database: SyncDatabase | None = None
    redis_client: redis.Redis | None = None
    item_index: IItemCandidateIndex | None = None


def _build_item_index(settings: Settings) -> IItemCandidateIndex:
    if settings.prefer_saved_faiss_index and settings.faiss_files_exist():
        return FaissItemIndex.load_saved(
            settings.faiss_index_path,
            settings.faiss_ids_path,
        )

    index = FaissItemIndex.from_embeddings_file(settings.als_item_embeddings_path)
    index.save(settings.faiss_index_path, settings.faiss_ids_path)
    return index


def _build_feature_repositories(
    settings: Settings,
    sync_db: SyncDatabase | None,
) -> tuple[
    IUserFeaturesRepository,
    IItemFeaturesRepository,
    IUserItemFeaturesRepository,
    IItemCatalogRepository,
]:
    if settings.repository_backend == "postgres":
        if sync_db is None:
            raise ValueError("sync_database is required for postgres backend")
        session_factory = sync_db.session_factory
        return (
            PostgresUserFeaturesRepository(session_factory),
            PostgresItemFeaturesRepository(session_factory),
            PostgresUserItemFeaturesRepository(session_factory),
            PostgresItemCatalogRepository(session_factory),
        )

    return (
        FileUserFeaturesRepository(settings.user_features_path, USER_FEATURE_KEYS),
        FileItemFeaturesRepository(settings.item_features_path, ITEM_FEATURE_KEYS),
        FileUserItemFeaturesRepository(
            settings.user_item_features_path, USER_ITEM_FEATURE_KEYS
        ),
        FileItemCatalogRepository(settings.item_catalog_path),
    )


def build_container(settings: Settings | None = None) -> AppContainer:
    settings = settings or get_settings()

    if settings.run_migrations_on_startup:
        run_migrations(settings.database_url_sync)

    sync_db: SyncDatabase | None = None
    if settings.repository_backend == "postgres":
        sync_db = create_sync_database(settings)

    redis_client = create_redis_client(settings)
    user_embeddings = RedisUserEmbeddingRepository(
        redis_client,
        key_prefix=settings.redis_user_embedding_key_prefix,
    )
    item_index = _build_item_index(settings)

    user_features, item_features, user_item_features, item_catalog = (
        _build_feature_repositories(settings, sync_db)
    )

    candidate_generator: ICandidateGenerator = IALSCandidateGenerator(
        user_embeddings,
        item_index,
    )
    ranker: IRanker = CatBoostRankerModel(
        settings.ranker_model_path,
        user_features,
        item_features,
        user_item_features,
        item_catalog,
        settings,
    )

    service = RecommendationService(candidate_generator, ranker)
    return AppContainer(
        settings=settings,
        recommendation_service=service,
        sync_database=sync_db,
        redis_client=redis_client,
        item_index=item_index,
    )
