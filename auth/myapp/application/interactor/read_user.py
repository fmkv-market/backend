from myapp.application.dto.user import UserID
from myapp.application.interface.user import UserReader


class ReadUserInteractor:
    def __init__(self, user_manager: UserReader):
        self.user_manager = user_manager


    def __call__(self, data: UserID):
        return self.user_manager.read_one(data)



