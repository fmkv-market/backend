from collections.abc import AsyncGenerator, Callable

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings

SessionFactory = Callable[[], Session]


class SyncDatabase:
    def __init__(self, database_url: str, *, echo: bool = False) -> None:
        self.engine: Engine = create_engine(
            database_url, echo=echo, pool_pre_ping=True
        )
        self.session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )


def create_sync_database(settings: Settings) -> SyncDatabase:
    return SyncDatabase(settings.database_url_sync, echo=settings.debug)


def create_async_session_factory(
    settings: Settings,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.database_url, echo=settings.debug)
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
