from abc import ABC, abstractmethod

from app.domain.entities import Candidate, RankedItem


class IRanker(ABC):
    @abstractmethod
    def rank(
        self,
        user_id: str,
        candidates: list[Candidate],
        top_k: int,
    ) -> list[RankedItem]:
        ...
        """Score and sort candidates for a single user."""
