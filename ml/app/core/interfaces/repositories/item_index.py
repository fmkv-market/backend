from abc import ABC, abstractmethod

import numpy as np


class IItemCandidateIndex(ABC):
    @abstractmethod
    def search(self, query_vector: np.ndarray, k: int) -> list[tuple[str, float]]:
        """Return (item_id, score) pairs sorted by relevance (higher is better)."""
