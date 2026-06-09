from typing import TypeVar

from pydantic import BaseModel

from myapp.infrastructure.database import Base


B_DTO = TypeVar("B_DTO", bound="BaseDTO")

class BaseDTO(BaseModel):

    @classmethod
    def map_to_domain_entity(cls, data: Base) -> B_DTO:
        return cls.model_validate(data, from_attributes=True)
