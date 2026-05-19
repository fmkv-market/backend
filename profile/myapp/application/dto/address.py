from myapp.application.dto.base import BaseDTO


class AddressCreate(BaseDTO):
    profile_id: int
    label: str | None = None
    country: str
    city: str
    street: str
    house: str
    apartment: str | None = None
    entrance: str | None = None
    floor: int | None = None
    intercom: str | None = None


class AddressData(AddressCreate):
    id: int
    is_default: bool

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.model_validate(data, from_attributes=True)
