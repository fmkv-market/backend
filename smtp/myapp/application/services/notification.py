from myapp.application.interface.sender import ISender


class NotificationService:
    """
    Контекст паттерна Стратегия.
    Не знает о конкретном канале — работает только через ISender.
    Стратегия подставляется через DI (Dishka).
    """

    def __init__(self, sender: ISender):
        self._sender = sender

    def set_sender(self, sender: ISender) -> None:
        """Позволяет менять стратегию в runtime."""
        self._sender = sender

    async def notify(self, recipients: list[str], message: str) -> None:
        await self._sender.send(recipients=recipients, message=message)