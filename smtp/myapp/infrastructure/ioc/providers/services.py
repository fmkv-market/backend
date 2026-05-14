from dishka import provide, Provider, Scope

from myapp.application.services.sender import EmailSender

class SenderProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def get_password_manager(self) -> EmailSender:
        return EmailSender()
