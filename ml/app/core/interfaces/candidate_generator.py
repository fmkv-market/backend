from abc import ABC, abstractmethod

from app.domain.entities import Candidate


class ICandidateGenerator(ABC):
    @abstractmethod
    def generate(self, user_id: str, n: int) -> list[Candidate]:
        """Return up to n candidate item ids for the user."""
