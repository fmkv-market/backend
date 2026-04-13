from myapp.application.dto.base import BaseDTO


class JWTData(BaseDTO):
    value: str

class Payload(BaseDTO):
    id: int
