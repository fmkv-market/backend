from pydantic import EmailStr, BaseModel

from myapp.controllers.schemas.base import UserLogin

type OTP = str

class EmailUserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class EmailUserLogin(UserLogin):
    email: EmailStr
    password: str


class EmailVerify(BaseModel):
    email: EmailStr
    code: OTP


class AccountDelete(BaseModel):
    email: EmailStr
    password: str


class AdminPasswordReset(BaseModel):
    new_password: str