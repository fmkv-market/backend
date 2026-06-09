import pickle
from pathlib import Path

import faiss
import numpy as np

from app.core.interfaces.repositories.item_index import IItemCandidateIndex


class FaissItemIndex(IItemCandidateIndex):

    def __init__(self, embeddings: dict[object, np.ndarray]) -> None:
        if not embeddings:
            raise ValueError("embeddings dict is empty")

        # ids can come as numpy uint64 / python int -> normalize to str
        items: list[tuple[str, np.ndarray]] = [(str(k), v) for k, v in embeddings.items()]
        self._item_ids = [item_id for item_id, _ in items]
        matrix = np.stack([vec for _, vec in items], axis=0).astype(np.float32)
        dim = matrix.shape[1]

        self._index = faiss.IndexFlatIP(dim)
        self._index.add(matrix)

    @classmethod
    def from_embeddings_file(cls, path: Path) -> "FaissItemIndex":
        with path.open("rb") as f:
            embeddings: dict[object, np.ndarray] = pickle.load(f)
        return cls(embeddings)

    def save(self, index_path: Path, ids_path: Path) -> None:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(index_path))
        with ids_path.open("wb") as f:
            pickle.dump(self._item_ids, f)

    @classmethod
    def load_saved(cls, index_path: Path, ids_path: Path) -> "FaissItemIndex":
        instance = cls.__new__(cls)
        instance._index = faiss.read_index(str(index_path))
        with ids_path.open("rb") as f:
            instance._item_ids = pickle.load(f)
        return instance

    def search(self, query_vector: np.ndarray, k: int) -> list[tuple[str, float]]:
        if k <= 0:
            return []
        k = min(k, len(self._item_ids))
        query = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)
        scores, indices = self._index.search(query, k)
        return [
            (self._item_ids[int(idx)], float(scores[0][i]))
            for i, idx in enumerate(indices[0])
            if int(idx) >= 0
        ]
