from pydantic import BaseModel, EmailStr

from myapp.application.dto.base import BaseDTO


class User(BaseDTO):
    phone: str | None = None
    email: EmailStr



class UserCreate(User):
    hash_password: str


class UserID(BaseModel):
    id: int

class UserData(User):
    id: int
    hash_password: str
    is_blocked: bool = False

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.model_validate(data, from_attributes=True)

class EmailLogin(BaseDTO):
    email: EmailStr
    password: str

class EmailVerifyDTO(BaseDTO):
    email: EmailStr
    otp: str