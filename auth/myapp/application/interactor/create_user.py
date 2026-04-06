from myapp.application.dto.user import UserCreate
from myapp.application.interface.user import UserSaver


class CreateUserInteractor:
    def __init__(self, user_manager: UserSaver) -> None:
        self.user_manager = user_manager


    def __call__(self, data: UserCreate):
        return self.user_manager.save(data)
