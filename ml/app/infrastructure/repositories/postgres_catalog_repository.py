from sqlalchemy.orm import Session, sessionmaker

from app.core.interfaces.repositories.catalog import IItemCatalogRepository
from app.infrastructure.db.models import ItemCatalog


class PostgresItemCatalogRepository(IItemCatalogRepository):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def get_product_category(self, item_id: int) -> str | None:
        with self._session_factory() as session:
            entity = session.get(ItemCatalog, item_id)
        if entity is None:
            return None
        return entity.product_category
