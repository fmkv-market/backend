from typing import Protocol



class IPasswordManager(Protocol):
    async def verify_password(self, plain_password, hashed_password) -> bool: pass

    async def hash_password(self, password: str) -> str: pass