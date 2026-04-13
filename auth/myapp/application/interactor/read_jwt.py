from myapp.application.dto.jwt import JWTData
from myapp.application.interface.jwt_manager import IJWTManager

class DecodeJWTInteractor:
    def __init__(self, jwt_manager: IJWTManager):
        self._jwt_manager = jwt_manager


    async def __call__(self, token: JWTData) -> dict[str, str]:
        return self._jwt_manager.read_jwt(token)