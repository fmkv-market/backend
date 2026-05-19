from dishka import provide, Provider, Scope

from myapp.infrastructure.config import Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_settings(self) -> Settings:
        return Settings()