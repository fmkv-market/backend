from myapp.application.dto.jwt import JWTData
from myapp.application.interface.jwt_manager import IJWTManager


class CreateJWTInteractor:
    def __init__(self, jwt_manager: IJWTManager) -> None:
        self._jwt_manager = jwt_manager

    async def __call__(self, data: dict) -> JWTData:
        return self._jwt_manager.create_jwt(data)
