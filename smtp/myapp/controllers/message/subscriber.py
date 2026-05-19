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
    print("start")
    await service.send(recipients=[msg["email"]], subject=msg["otp"])
    print("goood")



@router.subscriber(QueueConfig.sms_queue)
@faststream_inject
async def handle_verify_sms(
    msg: dict,
    sms_sender: FromDishka[SmsSender],
    service: FromDishka[NotificationService],
) -> None:
    service.set_sender(sms_sender)
    await service.notify(
        recipients=[msg["phone"]],
        message=msg["otp"],
    )