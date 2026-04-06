from pydantic import BaseModel


class User(BaseModel):
    name: str
    phone: str
    email: str


class UserCreate(User):
    hash_password: str


class UserID(BaseModel):
    id: int

class UserData(User):
    id: int

