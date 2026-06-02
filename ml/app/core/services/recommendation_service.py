from app.core.interfaces.candidate_generator import ICandidateGenerator
from app.core.interfaces.ranker import IRanker
from app.domain.entities import (
    RecommendationRequest,
    RecommendationResult,
)


class RecommendationService:
    def __init__(
        self,
        candidate_generator: ICandidateGenerator,
        ranker: IRanker,
    ) -> None:
        self._candidate_generator = candidate_generator
        self._ranker = ranker

    def recommend(self, request: RecommendationRequest) -> RecommendationResult:
        candidates = self._candidate_generator.generate(
            request.user_id,
            request.n_candidates,
        )
        if not candidates:
            return RecommendationResult(user_id=request.user_id, items=[])

        ranked = self._ranker.rank(
            request.user_id,
            candidates,
            request.top_k,
        )
        return RecommendationResult(user_id=request.user_id, items=ranked)
