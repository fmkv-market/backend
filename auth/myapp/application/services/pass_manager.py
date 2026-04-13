from passlib.context import CryptContext
from pwdlib import PasswordHash

from myapp.application.interface.pass_manager import IPasswordManager


class PasswordManager(IPasswordManager):
    pwd_context = PasswordHash.recommended()

    def __init__(self, context: CryptContext | None = None):
        if context:
            self.pwd_context = context

    async def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)