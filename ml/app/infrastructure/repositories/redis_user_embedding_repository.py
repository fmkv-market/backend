import pickle

import numpy as np
import redis

from app.core.interfaces.repositories.user_embeddings import IUserEmbeddingRepository


class RedisUserEmbeddingRepository(IUserEmbeddingRepository):
    def __init__(
        self,
        client: redis.Redis,
        key_prefix: str = "user_emb",
    ) -> None:
        self._client = client
        self._key_prefix = key_prefix

    def _key(self, user_id: str) -> str:
        return f"{self._key_prefix}:{user_id}"

    def get_user_embedding(self, user_id: str) -> np.ndarray | None:
        raw = self._client.get(self._key(user_id))
        if raw is None:
            return None
        return pickle.loads(raw)
