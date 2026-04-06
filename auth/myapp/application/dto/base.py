from pydantic import BaseModel

from myapp.infrastructure.database import Base
from myapp.infrastructure.hints import B_DTO


class BaseDTO(BaseModel):

    @classmethod
    def map_to_domain_entity(cls, data: Base) -> B_DTO:
        return cls.model_validate(data, from_attributes=True)
