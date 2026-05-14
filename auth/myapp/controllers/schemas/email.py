from pydantic import EmailStr, BaseModel

from myapp.controllers.schemas.base import UserRegister, UserLogin

type OTP = str

class EmailUserRegister(UserRegister):
    email: EmailStr
    password: str


class EmailUserLogin(UserLogin):
    email: EmailStr
    password: str


class EmailVerify(BaseModel):
    email: EmailStr
    code: OTP