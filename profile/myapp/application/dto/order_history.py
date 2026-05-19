from datetime import datetime
from decimal import Decimal
from typing import Any

from myapp.application.dto.base import BaseDTO


class OrderHistoryCreate(BaseDTO):
    profile_id: int
    order_id: int
    total_amount: Decimal
    status: str
    items: dict[str, Any]


class OrderHistoryData(OrderHistoryCreate):
    id: int
    created_at: datetime

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.model_validate(data, from_attributes=True)
