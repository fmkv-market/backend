from pydantic import BaseModel


class AddressCreateRequest(BaseModel):
    label: str | None = None
    country: str
    city: str
    street: str
    house: str
    apartment: str | None = None
    entrance: str | None = None
    floor: int | None = None
    intercom: str | None = None


class AddressResponse(AddressCreateRequest):
    id: int
    profile_id: int
    is_default: bool
