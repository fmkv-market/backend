from app.core.interfaces.candidate_generator import ICandidateGenerator
from app.core.interfaces.repositories.item_index import IItemCandidateIndex
from app.core.interfaces.repositories.user_embeddings import IUserEmbeddingRepository
from app.domain.entities import Candidate
from app.core.constants import MOST_POP_ITEMS


class IALSCandidateGenerator(ICandidateGenerator):
    """
    iALS inference: user embedding from Redis, nearest items via FAISS (inner product).
    Unknown user → empty candidate list.
    """

    def __init__(
        self,
        user_embeddings: IUserEmbeddingRepository,
        item_index: IItemCandidateIndex,
    ) -> None:
        self._user_embeddings = user_embeddings
        self._item_index = item_index

    def generate(self, user_id: str, n: int) -> list[Candidate]:
        user_vec = self._user_embeddings.get_user_embedding(user_id)
        if user_vec is None:
            return [Candidate(item_id=item_id) for item_id in MOST_POP_ITEMS]

        hits = self._item_index.search(user_vec, n)
        return [
            Candidate(item_id=item_id, score=score)
            for item_id, score in hits
        ]
