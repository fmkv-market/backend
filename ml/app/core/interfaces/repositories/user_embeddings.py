from abc import ABC, abstractmethod

import numpy as np


class IUserEmbeddingRepository(ABC):
    @abstractmethod
    def get_user_embedding(self, user_id: str) -> np.ndarray | None:
        pass
