from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from dishka.integrations.faststream import inject as faststream_inject

from myapp.application.services.sender import EmailSender
from myapp.infrastructure.message.config import QueueConfig

router = RabbitRouter()

@router.subscriber(QueueConfig.email_queue)
@faststream_inject
async def handle_verify_email(
        msg: dict,
        service: FromDishka[EmailSender]
):
    await service.send(recipients=[msg["email"]], subject=msg["otp"])