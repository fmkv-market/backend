from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_recommendation_service
from app.api.schemas.recommendation import (
    RecommendationResponse,
    RecommendationResponseItem,
)
from app.core.services.recommendation_service import RecommendationService
from app.domain.entities import RecommendationRequest

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/users/{user_id}", response_model=RecommendationResponse)
def get_user_recommendations(
    user_id: str,
    n_candidates: Annotated[int, Query(ge=1, le=1000)] = 300,
    top_k: Annotated[int, Query(ge=1, le=100)] = 10,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    if top_k > n_candidates:
        raise HTTPException(
            status_code=400,
            detail="top_k cannot be greater than n_candidates",
        )

    result = service.recommend(
        RecommendationRequest(
            user_id=user_id,
            n_candidates=n_candidates,
            top_k=top_k,
        )
    )
    return RecommendationResponse(
        user_id=result.user_id,
        items=[
            RecommendationResponseItem(
                item_id=item.item_id,
                score=item.score,
                rank=item.rank,
            )
            for item in result.items
        ],
    )
