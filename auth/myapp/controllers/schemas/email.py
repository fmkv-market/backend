from pydantic import EmailStr

from myapp.controllers.schemas.base import UserRegister, UserLogin


class EmailUserRegister(UserRegister):
    email: EmailStr
    password: str


class EmailUserLogin(UserLogin):
    email: EmailStr
    password: str