from pydantic import BaseModel


class RecommendationResponseItem(BaseModel):
    item_id: str
    score: float
    rank: int


class RecommendationResponse(BaseModel):
    user_id: str
    items: list[RecommendationResponseItem]
