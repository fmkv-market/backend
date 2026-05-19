from datetime import date, datetime

from pydantic import BaseModel


class ProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    avatar_url: str | None
    created_at: datetime
