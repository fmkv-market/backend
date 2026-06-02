from functools import lru_cache

from fastapi import Request

from app.composition.container import AppContainer, build_container
from app.core.services.recommendation_service import RecommendationService


@lru_cache
def get_container() -> AppContainer:
    return build_container()


def get_recommendation_service(request: Request) -> RecommendationService:
    container: AppContainer | None = getattr(request.app.state, "container", None)
    if container is None:
        container = get_container()
    return container.recommendation_service
