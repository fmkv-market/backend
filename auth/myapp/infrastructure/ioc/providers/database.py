from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from myapp.infrastructure.config import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(settings.POSTGRES_URL)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
        async_session = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        async with async_session() as session:
            yield session