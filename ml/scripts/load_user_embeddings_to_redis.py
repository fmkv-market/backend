
from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import numpy as np
from tqdm import tqdm

from app.config import get_settings
from app.infrastructure.redis.client import create_redis_client


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=settings.als_user_embeddings_path,
    )
    parser.add_argument("--batch-size", type=int, default=5000)
    args = parser.parse_args()

    if not args.input.is_file():
        raise FileNotFoundError(f"Missing {args.input}")

    with args.input.open("rb") as f:
        embeddings: dict[object, np.ndarray] = pickle.load(f)

    client = create_redis_client(settings)
    prefix = settings.redis_user_embedding_key_prefix
    items = list(embeddings.items())

    for start in tqdm(range(0, len(items), args.batch_size)):
        pipe = client.pipeline()
        batch = items[start : start + args.batch_size]
        for user_id, vector in batch:
            pipe.set(
                f"{prefix}:{str(user_id)}",
                pickle.dumps(vector, protocol=pickle.HIGHEST_PROTOCOL),
            )
        pipe.execute()

    print(f"Loaded {len(items)} user embeddings into Redis ({prefix}:*)")


if __name__ == "__main__":
    main()
