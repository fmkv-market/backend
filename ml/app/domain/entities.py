from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Candidate:
    item_id: str
    score: float | None = None


@dataclass(frozen=True, slots=True)
class RankedItem:
    item_id: str
    score: float
    rank: int


@dataclass(slots=True)
class RecommendationRequest:
    user_id: str
    n_candidates: int = 300
    top_k: int = 10


@dataclass(slots=True)
class RecommendationResult:
    user_id: str
    items: list[RankedItem] = field(default_factory=list)
