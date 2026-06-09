from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response

from myapp.application.dto.user import UserCreate, EmailLogin, UserData, EmailVerifyDTO
from myapp.application.exception.password import PasswordValidationException
from myapp.application.exception.user import UserEmailAlreadyExistsException, UserEmailNotFoundException, UserBlockedException
from myapp.application.interactor.delete_user import DeleteUserInteractor
from myapp.application.interactor.login_user import EmailLoginUser
from myapp.application.interactor.register_user import EmailRegisterUser
from myapp.application.interface.pass_manager import IPasswordManager

from myapp.controllers.exceptions import UserEmailAlreadyExistsHTTPException, UserEmailNotExistsHTTPException, \
    IncorrectPasswordHTTPException, OTPInvalidHTTPException, UserBlockedHTTPException
from myapp.controllers.schemas.email import AccountDelete, EmailUserRegister, EmailVerify

router = APIRouter(prefix="/email", tags=["Авторизация и аутентификация"], route_class=DishkaRoute)
from logiro import setup_logger, LogConfig

setup_logger(LogConfig(level=20, json_enabled=True))

import logging

logger = logging.getLogger(__name__)


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
        user = await register_executor.register_user(register_dto, data.first_name, data.last_name)
    except UserEmailAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    login_dto = EmailLogin(email=data.email, password=data.password)
    try:
        jwt = await login_executor.login_user(login_dto)

    except UserEmailNotFoundException:
        raise UserEmailNotExistsHTTPException
    except PasswordValidationException:
        raise IncorrectPasswordHTTPException
    logger.info("Пользователь создан")

    response.set_cookie("access_token", jwt.value)
    return user


@router.post("/login_email", summary="Авторизация пользователя через почту")
async def login_user_by_email(
        login_executor: FromDishka[EmailLoginUser],
        data: EmailUserRegister,
) -> Response:
    login_dto = EmailLogin(email=data.email, password=data.password)
    try:
        await login_executor.request_login(login_dto)
    except UserEmailNotFoundException:
        raise UserEmailNotExistsHTTPException
    except UserBlockedException:
        raise UserBlockedHTTPException
    except PasswordValidationException:
        raise IncorrectPasswordHTTPException
    return Response(status_code=200)


@router.post("/verify-email", summary="Подтверждение email")
async def verify_email(
        login_executor: FromDishka[EmailLoginUser],
        data: EmailVerify,
        response: Response,
) -> Response:
    verify_dto = EmailVerifyDTO(email=data.email, otp=data.code)
    try:
        jwt = await login_executor.verify_email(verify_dto)
    except OTPInvalidHTTPException:
        raise OTPInvalidHTTPException
    response.set_cookie("access_token", jwt.value)
    return Response(status_code=200)


@router.post("/logout", summary="Выход из системы")
async def logout(response: Response) -> Response:
    response.delete_cookie("access_token")
    return Response(status_code=200)


@router.delete("/account", summary="Удаление учётной записи (с подтверждением паролем)")
async def delete_account(
        delete_executor: FromDishka[DeleteUserInteractor],
        data: AccountDelete,
        response: Response,
) -> Response:
    try:
        await delete_executor.execute(email=data.email, password=data.password)
    except UserEmailNotFoundException:
        raise UserEmailNotExistsHTTPException
    except PasswordValidationException:
        raise IncorrectPasswordHTTPException
    response.delete_cookie("access_token")
    return Response(status_code=204)
