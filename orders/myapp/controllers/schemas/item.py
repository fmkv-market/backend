from pydantic import BaseModel


class RequestItemInfo(BaseModel):
    item_id: int
    cost: float
    quantity: int = 1
    cart_id: int