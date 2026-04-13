from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response

from myapp.application.dto.jwt import JWTData
from myapp.application.dto.user import UserCreate, EmailLogin, UserData
from myapp.application.exception.password import PasswordValidationException
from myapp.application.exception.user import UserEmailAlreadyExistsException, UserEmailNotFoundException
from myapp.application.interactor.login_user import EmailLoginUser
from myapp.application.interactor.register_user import EmailRegisterUser
from myapp.application.interface.pass_manager import IPasswordManager

from myapp.application.services.pass_manager import PasswordManager
from myapp.controllers.exceptions import UserEmailAlreadyExistsHTTPException, UserEmailNotExistsHTTPException, \
    IncorrectPasswordHTTPException
from myapp.controllers.schemas.email import EmailUserRegister

router = APIRouter(prefix="/email", tags=["Авторизация и аутентификация"], route_class=DishkaRoute)


@router.post("/register_email", summary="Регистрация пользователя через почту")
async def register_user_by_email(
        register_executor: FromDishka[EmailRegisterUser],
        login_executor: FromDishka[EmailLoginUser],
        pass_manager: FromDishka[IPasswordManager],
        data: EmailUserRegister,
        response: Response,
) -> UserData:
    hashed_password = await pass_manager.hash_password(data.password)
    register_dto = UserCreate(email=data.email, hash_password=hashed_password)

    try:
        user = await register_executor.register_user(register_dto)
    except UserEmailAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    login_dto = EmailLogin(email=data.email, password=data.password)
    try:
        jwt = await login_executor.login_user(login_dto)
    except UserEmailNotFoundException:
        raise UserEmailNotExistsHTTPException
    except PasswordValidationException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", jwt.value)
    return user


@router.post("/login_email", summary="Авторизация пользователя через почту")
async def login_user_by_email(
        login_executor: FromDishka[EmailLoginUser],
        data: EmailUserRegister,
        response: Response,
) -> Response:
    login_dto = EmailLogin(email=data.email, password=data.password)
    try:
        jwt = await login_executor.login_user(login_dto)
    except UserEmailNotFoundException:
        raise UserEmailNotExistsHTTPException
    except PasswordValidationException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", jwt.value)
    return Response(status_code=200)