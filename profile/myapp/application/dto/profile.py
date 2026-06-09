from datetime import date, datetime

from myapp.application.dto.base import BaseDTO


class ProfileCreate(BaseDTO):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None


class ProfileUpdate(BaseDTO):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None


class ProfileData(BaseDTO):
    id: int
    user_id: int
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    avatar_url: str | None
    created_at: datetime

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.model_validate(data, from_attributes=True)
