from pydantic import BaseModel, EmailStr

from myapp.application.dto.base import BaseDTO


class User(BaseModel):
    phone: str
    email: EmailStr


class UserCreate(User):
    hash_password: str


class UserID(BaseModel):
    id: int

class UserData(User):
    id: int

class EmailLogin(BaseDTO):
    email: EmailStr
    password: str